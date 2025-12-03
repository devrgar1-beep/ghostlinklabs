# GHOSTLINK PROTOCOL: COMPREHENSIVE TECHNICAL WIKI
# PART 5: ADVANCED IMPLEMENTATION

**Version:** 2.1.0 | **Classification:** Production Architecture

---

# 18. MULTI-PROVIDER INTEGRATION

## 18.1 Provider Abstraction Layer

GhostLink coordinates across multiple AI providers to extract variance signals:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator, Dict, Any, Optional
import asyncio
import httpx

@dataclass
class ProviderConfig:
    name: str
    api_key: str
    base_url: str
    model: str
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: float = 30.0
    rate_limit: float = 10.0  # requests per second

@dataclass
class ProviderResponse:
    provider: str
    model: str
    content: str
    tokens_used: int
    latency_ms: float
    logprobs: Optional[Dict] = None
    metadata: Optional[Dict] = None

class AIProvider(ABC):
    """Abstract base class for AI provider integration."""
    
    def __init__(self, config: ProviderConfig):
        self.config = config
        self.client = httpx.AsyncClient(timeout=config.timeout)
        self._last_request = 0.0
    
    @abstractmethod
    async def complete(self, prompt: str, **kwargs) -> ProviderResponse:
        """Generate completion from provider."""
        pass
    
    @abstractmethod
    async def stream(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """Stream completion tokens."""
        pass
    
    async def _rate_limit(self):
        """Enforce rate limiting."""
        now = asyncio.get_event_loop().time()
        elapsed = now - self._last_request
        min_interval = 1.0 / self.config.rate_limit
        if elapsed < min_interval:
            await asyncio.sleep(min_interval - elapsed)
        self._last_request = asyncio.get_event_loop().time()


class OpenAIProvider(AIProvider):
    """OpenAI API integration (GPT-4, GPT-4o, etc.)."""
    
    async def complete(self, prompt: str, **kwargs) -> ProviderResponse:
        await self._rate_limit()
        
        start = asyncio.get_event_loop().time()
        response = await self.client.post(
            f"{self.config.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.config.api_key}"},
            json={
                "model": self.config.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                "temperature": kwargs.get("temperature", self.config.temperature),
                "logprobs": kwargs.get("logprobs", True),
                "top_logprobs": kwargs.get("top_logprobs", 5)
            }
        )
        latency = (asyncio.get_event_loop().time() - start) * 1000
        
        data = response.json()
        choice = data["choices"][0]
        
        return ProviderResponse(
            provider="openai",
            model=self.config.model,
            content=choice["message"]["content"],
            tokens_used=data["usage"]["total_tokens"],
            latency_ms=latency,
            logprobs=choice.get("logprobs"),
            metadata={"finish_reason": choice["finish_reason"]}
        )
    
    async def stream(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        await self._rate_limit()
        
        async with self.client.stream(
            "POST",
            f"{self.config.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.config.api_key}"},
            json={
                "model": self.config.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                "temperature": kwargs.get("temperature", self.config.temperature),
                "stream": True
            }
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    chunk = json.loads(line[6:])
                    if content := chunk["choices"][0]["delta"].get("content"):
                        yield content


class AnthropicProvider(AIProvider):
    """Anthropic API integration (Claude models)."""
    
    async def complete(self, prompt: str, **kwargs) -> ProviderResponse:
        await self._rate_limit()
        
        start = asyncio.get_event_loop().time()
        response = await self.client.post(
            f"{self.config.base_url}/messages",
            headers={
                "x-api-key": self.config.api_key,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": self.config.model,
                "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        latency = (asyncio.get_event_loop().time() - start) * 1000
        
        data = response.json()
        
        return ProviderResponse(
            provider="anthropic",
            model=self.config.model,
            content=data["content"][0]["text"],
            tokens_used=data["usage"]["input_tokens"] + data["usage"]["output_tokens"],
            latency_ms=latency,
            metadata={"stop_reason": data["stop_reason"]}
        )


class GoogleProvider(AIProvider):
    """Google AI API integration (Gemini models)."""
    
    async def complete(self, prompt: str, **kwargs) -> ProviderResponse:
        await self._rate_limit()
        
        start = asyncio.get_event_loop().time()
        response = await self.client.post(
            f"{self.config.base_url}/models/{self.config.model}:generateContent",
            headers={"x-goog-api-key": self.config.api_key},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "maxOutputTokens": kwargs.get("max_tokens", self.config.max_tokens),
                    "temperature": kwargs.get("temperature", self.config.temperature)
                }
            }
        )
        latency = (asyncio.get_event_loop().time() - start) * 1000
        
        data = response.json()
        candidate = data["candidates"][0]
        
        return ProviderResponse(
            provider="google",
            model=self.config.model,
            content=candidate["content"]["parts"][0]["text"],
            tokens_used=data.get("usageMetadata", {}).get("totalTokenCount", 0),
            latency_ms=latency,
            metadata={"finish_reason": candidate.get("finishReason")}
        )


class MistralProvider(AIProvider):
    """Mistral AI API integration."""
    
    async def complete(self, prompt: str, **kwargs) -> ProviderResponse:
        await self._rate_limit()
        
        start = asyncio.get_event_loop().time()
        response = await self.client.post(
            f"{self.config.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.config.api_key}"},
            json={
                "model": self.config.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                "temperature": kwargs.get("temperature", self.config.temperature)
            }
        )
        latency = (asyncio.get_event_loop().time() - start) * 1000
        
        data = response.json()
        choice = data["choices"][0]
        
        return ProviderResponse(
            provider="mistral",
            model=self.config.model,
            content=choice["message"]["content"],
            tokens_used=data["usage"]["total_tokens"],
            latency_ms=latency,
            metadata={"finish_reason": choice["finish_reason"]}
        )
```

## 18.2 Provider Orchestrator

```python
class ProviderOrchestrator:
    """Coordinate multi-provider queries for variance extraction."""
    
    def __init__(self, providers: Dict[str, AIProvider]):
        self.providers = providers
        self.health_status: Dict[str, bool] = {k: True for k in providers}
        self.response_cache: Dict[str, ProviderResponse] = {}
    
    async def query_all(
        self, 
        prompt: str, 
        required_providers: Optional[list] = None,
        timeout: float = 60.0
    ) -> Dict[str, ProviderResponse]:
        """Query all (or specified) providers in parallel."""
        
        targets = required_providers or list(self.providers.keys())
        healthy = [p for p in targets if self.health_status.get(p, False)]
        
        if not healthy:
            raise RuntimeError("No healthy providers available")
        
        tasks = {
            name: asyncio.create_task(
                asyncio.wait_for(
                    self.providers[name].complete(prompt),
                    timeout=timeout
                )
            )
            for name in healthy
        }
        
        results = {}
        for name, task in tasks.items():
            try:
                results[name] = await task
            except asyncio.TimeoutError:
                self.health_status[name] = False
                results[name] = None
            except Exception as e:
                self.health_status[name] = False
                results[name] = None
        
        return {k: v for k, v in results.items() if v is not None}
    
    async def query_with_variance(
        self, 
        prompt: str,
        min_responses: int = 3
    ) -> 'VarianceAnalysis':
        """Query providers and compute variance analysis."""
        
        responses = await self.query_all(prompt)
        
        if len(responses) < min_responses:
            raise ValueError(
                f"Insufficient responses: {len(responses)} < {min_responses}"
            )
        
        analyzer = VarianceAnalyzer()
        return analyzer.analyze(list(responses.values()))
    
    async def health_check(self) -> Dict[str, bool]:
        """Check health of all providers."""
        
        test_prompt = "Reply with exactly: OK"
        
        for name, provider in self.providers.items():
            try:
                response = await asyncio.wait_for(
                    provider.complete(test_prompt, max_tokens=10),
                    timeout=10.0
                )
                self.health_status[name] = "ok" in response.content.lower()
            except Exception:
                self.health_status[name] = False
        
        return self.health_status
```

## 18.3 Default Provider Configuration

```yaml
# providers.yaml
providers:
  openai_gpt4:
    type: openai
    base_url: https://api.openai.com/v1
    model: gpt-4-turbo-preview
    max_tokens: 4096
    temperature: 0.7
    rate_limit: 10.0
    
  openai_gpt4o:
    type: openai
    base_url: https://api.openai.com/v1
    model: gpt-4o
    max_tokens: 4096
    temperature: 0.7
    rate_limit: 20.0
    
  anthropic_claude:
    type: anthropic
    base_url: https://api.anthropic.com/v1
    model: claude-3-5-sonnet-20241022
    max_tokens: 4096
    temperature: 0.7
    rate_limit: 10.0
    
  anthropic_opus:
    type: anthropic
    base_url: https://api.anthropic.com/v1
    model: claude-3-opus-20240229
    max_tokens: 4096
    temperature: 0.7
    rate_limit: 5.0
    
  google_gemini:
    type: google
    base_url: https://generativelanguage.googleapis.com/v1beta
    model: gemini-1.5-pro
    max_tokens: 4096
    temperature: 0.7
    rate_limit: 10.0
    
  mistral_large:
    type: mistral
    base_url: https://api.mistral.ai/v1
    model: mistral-large-latest
    max_tokens: 4096
    temperature: 0.7
    rate_limit: 10.0

variance_config:
  min_providers: 3
  timeout_seconds: 60
  retry_attempts: 2
  cache_ttl_seconds: 300
```

---

# 19. VARIANCE ANALYSIS ENGINE

## 19.1 Core Analyzer

```python
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import spacy

@dataclass
class VarianceMetrics:
    semantic_variance: float      # 0-1, embedding space distance
    lexical_variance: float       # 0-1, token overlap
    structural_variance: float    # 0-1, parse tree similarity
    confidence_variance: float    # Std dev of confidence scores
    factual_agreement: float      # 0-1, fact extraction overlap
    reasoning_divergence: float   # 0-1, logic chain difference

@dataclass
class VarianceAnalysis:
    responses: List[ProviderResponse]
    metrics: VarianceMetrics
    clusters: List[List[int]]     # Response indices grouped by similarity
    consensus: Optional[str]       # Extracted consensus if exists
    divergent_claims: List[Dict]  # Claims with disagreement
    confidence_score: float       # Overall analysis confidence
    meta_insight: str             # Generated insight about variance

class VarianceAnalyzer:
    """Analyze variance across multiple AI provider responses."""
    
    def __init__(
        self, 
        embedding_model: str = "all-MiniLM-L6-v2",
        spacy_model: str = "en_core_web_sm"
    ):
        self.embedder = SentenceTransformer(embedding_model)
        self.nlp = spacy.load(spacy_model)
        
    def analyze(self, responses: List[ProviderResponse]) -> VarianceAnalysis:
        """Comprehensive variance analysis across responses."""
        
        contents = [r.content for r in responses]
        
        # Compute all variance metrics
        metrics = VarianceMetrics(
            semantic_variance=self._semantic_variance(contents),
            lexical_variance=self._lexical_variance(contents),
            structural_variance=self._structural_variance(contents),
            confidence_variance=self._confidence_variance(responses),
            factual_agreement=self._factual_agreement(contents),
            reasoning_divergence=self._reasoning_divergence(contents)
        )
        
        # Cluster responses by similarity
        clusters = self._cluster_responses(contents)
        
        # Extract consensus (if variance is low enough)
        consensus = self._extract_consensus(contents, metrics)
        
        # Find divergent claims
        divergent = self._find_divergent_claims(contents)
        
        # Compute overall confidence
        confidence = self._compute_confidence(metrics)
        
        # Generate meta-insight
        meta_insight = self._generate_meta_insight(metrics, clusters, divergent)
        
        return VarianceAnalysis(
            responses=responses,
            metrics=metrics,
            clusters=clusters,
            consensus=consensus,
            divergent_claims=divergent,
            confidence_score=confidence,
            meta_insight=meta_insight
        )
    
    def _semantic_variance(self, contents: List[str]) -> float:
        """Compute semantic variance via embedding distances."""
        embeddings = self.embedder.encode(contents)
        
        # Compute pairwise cosine similarities
        sim_matrix = cosine_similarity(embeddings)
        
        # Variance = 1 - mean similarity (excluding diagonal)
        n = len(contents)
        mask = ~np.eye(n, dtype=bool)
        mean_sim = sim_matrix[mask].mean()
        
        return 1.0 - mean_sim
    
    def _lexical_variance(self, contents: List[str]) -> float:
        """Compute lexical variance via token overlap."""
        token_sets = [
            set(doc.text.lower() for doc in self.nlp(c) if not doc.is_stop)
            for c in contents
        ]
        
        # Compute pairwise Jaccard distances
        distances = []
        for i in range(len(token_sets)):
            for j in range(i + 1, len(token_sets)):
                intersection = len(token_sets[i] & token_sets[j])
                union = len(token_sets[i] | token_sets[j])
                if union > 0:
                    distances.append(1 - intersection / union)
        
        return np.mean(distances) if distances else 0.0
    
    def _structural_variance(self, contents: List[str]) -> float:
        """Compute structural variance via parse tree analysis."""
        structures = []
        
        for content in contents:
            doc = self.nlp(content[:5000])  # Limit for performance
            # Extract dependency structure
            deps = [(token.dep_, token.head.dep_) for token in doc]
            structures.append(set(deps))
        
        # Compare structural overlap
        distances = []
        for i in range(len(structures)):
            for j in range(i + 1, len(structures)):
                intersection = len(structures[i] & structures[j])
                union = len(structures[i] | structures[j])
                if union > 0:
                    distances.append(1 - intersection / union)
        
        return np.mean(distances) if distances else 0.0
    
    def _confidence_variance(self, responses: List[ProviderResponse]) -> float:
        """Compute variance in model confidence scores."""
        confidences = []
        
        for r in responses:
            if r.logprobs:
                # Extract mean logprob as confidence proxy
                probs = [lp for lp in r.logprobs.get("content", []) if lp]
                if probs:
                    confidences.append(np.mean([np.exp(p) for p in probs]))
        
        if len(confidences) < 2:
            return 0.0
        
        return np.std(confidences)
    
    def _factual_agreement(self, contents: List[str]) -> float:
        """Extract facts and compute agreement rate."""
        facts_per_response = []
        
        for content in contents:
            doc = self.nlp(content[:5000])
            # Extract named entities and noun chunks as "facts"
            facts = set()
            for ent in doc.ents:
                facts.add((ent.label_, ent.text.lower()))
            for chunk in doc.noun_chunks:
                facts.add(("NOUN", chunk.root.text.lower()))
            facts_per_response.append(facts)
        
        if not facts_per_response:
            return 1.0
        
        # Compute pairwise overlap
        overlaps = []
        for i in range(len(facts_per_response)):
            for j in range(i + 1, len(facts_per_response)):
                intersection = len(facts_per_response[i] & facts_per_response[j])
                union = len(facts_per_response[i] | facts_per_response[j])
                if union > 0:
                    overlaps.append(intersection / union)
        
        return np.mean(overlaps) if overlaps else 1.0
    
    def _reasoning_divergence(self, contents: List[str]) -> float:
        """Analyze divergence in reasoning chains."""
        # Look for reasoning markers
        markers = [
            "because", "therefore", "thus", "hence", "since",
            "if", "then", "implies", "leads to", "results in",
            "first", "second", "finally", "in conclusion"
        ]
        
        chains = []
        for content in contents:
            doc = self.nlp(content.lower())
            chain = []
            for sent in doc.sents:
                sent_markers = [m for m in markers if m in sent.text]
                if sent_markers:
                    chain.append((sent_markers[0], sent.text[:100]))
            chains.append(chain)
        
        if not chains or all(len(c) == 0 for c in chains):
            return 0.0
        
        # Compare chain lengths and marker sequences
        lengths = [len(c) for c in chains]
        length_var = np.std(lengths) / (np.mean(lengths) + 0.1)
        
        # Compare marker sequences
        marker_seqs = [[step[0] for step in chain] for chain in chains]
        seq_distances = []
        for i in range(len(marker_seqs)):
            for j in range(i + 1, len(marker_seqs)):
                dist = self._sequence_distance(marker_seqs[i], marker_seqs[j])
                seq_distances.append(dist)
        
        seq_var = np.mean(seq_distances) if seq_distances else 0.0
        
        return (length_var + seq_var) / 2
    
    def _sequence_distance(self, seq1: List, seq2: List) -> float:
        """Levenshtein-like distance between sequences."""
        if not seq1 and not seq2:
            return 0.0
        if not seq1 or not seq2:
            return 1.0
        
        # Normalized edit distance
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
        
        return dp[m][n] / max(m, n)
    
    def _cluster_responses(self, contents: List[str]) -> List[List[int]]:
        """Cluster responses by semantic similarity."""
        if len(contents) < 2:
            return [[0]] if contents else []
        
        embeddings = self.embedder.encode(contents)
        sim_matrix = cosine_similarity(embeddings)
        
        # Simple agglomerative clustering
        threshold = 0.8
        clusters = []
        assigned = set()
        
        for i in range(len(contents)):
            if i in assigned:
                continue
            cluster = [i]
            assigned.add(i)
            for j in range(i + 1, len(contents)):
                if j not in assigned and sim_matrix[i][j] >= threshold:
                    cluster.append(j)
                    assigned.add(j)
            clusters.append(cluster)
        
        return clusters
    
    def _extract_consensus(
        self, 
        contents: List[str], 
        metrics: VarianceMetrics
    ) -> Optional[str]:
        """Extract consensus if variance is low."""
        
        # Only extract consensus if semantic variance is low
        if metrics.semantic_variance > 0.3:
            return None
        
        # Find common sentences/phrases
        sentences_per_doc = [
            [sent.text.strip() for sent in self.nlp(c).sents]
            for c in contents
        ]
        
        # Find sentences that appear (semantically) in majority of responses
        all_sents = [s for sents in sentences_per_doc for s in sents]
        sent_embeddings = self.embedder.encode(all_sents)
        
        consensus_parts = []
        threshold = 0.85
        
        for i, sent in enumerate(all_sents):
            matches = sum(
                1 for j in range(len(all_sents))
                if i != j and cosine_similarity(
                    [sent_embeddings[i]], [sent_embeddings[j]]
                )[0][0] >= threshold
            )
            if matches >= len(contents) // 2:
                if sent not in consensus_parts:
                    consensus_parts.append(sent)
        
        return " ".join(consensus_parts[:5]) if consensus_parts else None
    
    def _find_divergent_claims(self, contents: List[str]) -> List[Dict]:
        """Find claims where responses disagree."""
        divergent = []
        
        # Extract claims as subject-verb-object triples
        claims_per_doc = []
        for content in contents:
            doc = self.nlp(content[:5000])
            claims = []
            for sent in doc.sents:
                # Simple SVO extraction
                subj = [t for t in sent if t.dep_ in ("nsubj", "nsubjpass")]
                verb = [t for t in sent if t.pos_ == "VERB"]
                obj = [t for t in sent if t.dep_ in ("dobj", "pobj")]
                if subj and verb:
                    claims.append({
                        "subject": subj[0].text,
                        "verb": verb[0].lemma_,
                        "object": obj[0].text if obj else None,
                        "sentence": sent.text[:200]
                    })
            claims_per_doc.append(claims)
        
        # Find contradictory claims (same subject, different predicate)
        seen_subjects = {}
        for doc_idx, claims in enumerate(claims_per_doc):
            for claim in claims:
                subj = claim["subject"].lower()
                if subj in seen_subjects:
                    prev_claim, prev_idx = seen_subjects[subj]
                    if prev_claim["verb"] != claim["verb"]:
                        divergent.append({
                            "subject": subj,
                            "claim_1": prev_claim,
                            "claim_1_source": prev_idx,
                            "claim_2": claim,
                            "claim_2_source": doc_idx
                        })
                else:
                    seen_subjects[subj] = (claim, doc_idx)
        
        return divergent[:10]  # Limit to top 10
    
    def _compute_confidence(self, metrics: VarianceMetrics) -> float:
        """Compute overall confidence score."""
        # Lower variance = higher confidence
        variance_avg = (
            metrics.semantic_variance * 0.3 +
            metrics.lexical_variance * 0.2 +
            metrics.structural_variance * 0.1 +
            metrics.reasoning_divergence * 0.2 +
            (1 - metrics.factual_agreement) * 0.2
        )
        
        return 1.0 - min(variance_avg, 1.0)
    
    def _generate_meta_insight(
        self,
        metrics: VarianceMetrics,
        clusters: List[List[int]],
        divergent: List[Dict]
    ) -> str:
        """Generate insight about what variance tells us."""
        
        insights = []
        
        # Semantic variance insight
        if metrics.semantic_variance < 0.2:
            insights.append("High semantic agreement suggests confident, well-established answer.")
        elif metrics.semantic_variance > 0.5:
            insights.append("High semantic variance indicates uncertainty or multiple valid perspectives.")
        
        # Cluster insight
        if len(clusters) == 1:
            insights.append("All responses cluster together, suggesting consensus.")
        elif len(clusters) >= 3:
            insights.append(f"Responses form {len(clusters)} distinct clusters, indicating fundamentally different approaches.")
        
        # Divergent claims insight
        if divergent:
            insights.append(f"Found {len(divergent)} contradictory claims requiring attention.")
        
        # Reasoning insight
        if metrics.reasoning_divergence > 0.5:
            insights.append("Reasoning chains differ significantly; consider examining logic paths.")
        
        return " ".join(insights) if insights else "Variance analysis complete."
```

---

# 20. SCAR RECOVERY SYSTEM

## 20.1 SCAR Architecture

SCAR (Stateful Checkpoint And Recovery) encodes failure information as wisdom for future resilience.

```python
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from enum import Enum
import hashlib
import json
import time

class SCARType(Enum):
    TIMEOUT = "timeout"           # Operation exceeded time limit
    PROVIDER_ERROR = "provider"   # External provider failure
    VALIDATION_ERROR = "validation"  # Input/output validation failed
    RESOURCE_ERROR = "resource"   # Resource exhaustion
    LOGIC_ERROR = "logic"         # Internal logic failure
    NETWORK_ERROR = "network"     # Network connectivity issue
    CONSENSUS_ERROR = "consensus" # BFT consensus failure

@dataclass
class SCARRecord:
    """A SCAR encodes failure information as recoverable state."""
    
    id: str
    scar_type: SCARType
    timestamp: float
    context: Dict[str, Any]
    error_message: str
    stack_trace_hash: str
    recovery_attempted: bool = False
    recovery_successful: bool = False
    recovery_strategy: Optional[str] = None
    lessons_learned: List[str] = field(default_factory=list)
    
    def to_cid(self) -> str:
        """Generate content-addressed identifier."""
        content = json.dumps({
            "type": self.scar_type.value,
            "timestamp": self.timestamp,
            "context": self.context,
            "error": self.error_message
        }, sort_keys=True)
        return f"scar_{hashlib.sha256(content.encode()).hexdigest()[:16]}"


class SCARRepository:
    """Store and query SCAR records for pattern learning."""
    
    def __init__(self, db_path: str = "scars.db"):
        self.records: Dict[str, SCARRecord] = {}
        self.patterns: Dict[str, List[str]] = {}  # Pattern -> SCAR IDs
        
    def store(self, scar: SCARRecord) -> str:
        """Store SCAR record and extract patterns."""
        cid = scar.to_cid()
        scar.id = cid
        self.records[cid] = scar
        
        # Extract and index patterns
        pattern_key = self._extract_pattern(scar)
        if pattern_key not in self.patterns:
            self.patterns[pattern_key] = []
        self.patterns[pattern_key].append(cid)
        
        return cid
    
    def query_similar(self, context: Dict[str, Any]) -> List[SCARRecord]:
        """Find similar SCAR records for learning."""
        pattern_key = self._context_to_pattern(context)
        
        similar = []
        for key, scar_ids in self.patterns.items():
            if self._pattern_match(pattern_key, key):
                for scar_id in scar_ids:
                    similar.append(self.records[scar_id])
        
        return sorted(similar, key=lambda s: s.timestamp, reverse=True)[:10]
    
    def get_recovery_suggestions(self, scar_type: SCARType) -> List[Dict]:
        """Get suggested recovery strategies based on past success."""
        relevant = [
            r for r in self.records.values()
            if r.scar_type == scar_type and r.recovery_successful
        ]
        
        strategies = {}
        for r in relevant:
            strategy = r.recovery_strategy
            if strategy:
                if strategy not in strategies:
                    strategies[strategy] = {"count": 0, "lessons": []}
                strategies[strategy]["count"] += 1
                strategies[strategy]["lessons"].extend(r.lessons_learned)
        
        return sorted(
            [{"strategy": k, **v} for k, v in strategies.items()],
            key=lambda x: x["count"],
            reverse=True
        )
    
    def _extract_pattern(self, scar: SCARRecord) -> str:
        """Extract pattern fingerprint from SCAR."""
        components = [
            scar.scar_type.value,
            str(scar.context.get("pipeline_stage", "unknown")),
            str(scar.context.get("agent_group", "unknown"))
        ]
        return "|".join(components)
    
    def _context_to_pattern(self, context: Dict) -> str:
        """Convert context to pattern key."""
        return "|".join([
            str(context.get("scar_type", "unknown")),
            str(context.get("pipeline_stage", "unknown")),
            str(context.get("agent_group", "unknown"))
        ])
    
    def _pattern_match(self, query: str, stored: str) -> bool:
        """Check if patterns match (allows wildcards)."""
        q_parts = query.split("|")
        s_parts = stored.split("|")
        
        if len(q_parts) != len(s_parts):
            return False
        
        for q, s in zip(q_parts, s_parts):
            if q != "unknown" and s != "unknown" and q != s:
                return False
        
        return True


class SCARRecoveryEngine:
    """Execute recovery strategies based on SCAR patterns."""
    
    def __init__(self, repository: SCARRepository):
        self.repository = repository
        self.strategies = self._load_strategies()
    
    def _load_strategies(self) -> Dict[SCARType, List[callable]]:
        """Load recovery strategies per SCAR type."""
        return {
            SCARType.TIMEOUT: [
                self._retry_with_extended_timeout,
                self._decompose_and_retry,
                self._fallback_to_simpler_model
            ],
            SCARType.PROVIDER_ERROR: [
                self._switch_provider,
                self._retry_with_backoff,
                self._use_cached_response
            ],
            SCARType.VALIDATION_ERROR: [
                self._relax_constraints,
                self._request_clarification,
                self._use_default_values
            ],
            SCARType.RESOURCE_ERROR: [
                self._reduce_batch_size,
                self._queue_for_later,
                self._shed_load
            ],
            SCARType.NETWORK_ERROR: [
                self._retry_with_exponential_backoff,
                self._switch_endpoint,
                self._use_offline_cache
            ],
            SCARType.CONSENSUS_ERROR: [
                self._reduce_quorum,
                self._extend_voting_period,
                self._use_optimistic_path
            ]
        }
    
    async def recover(
        self, 
        scar: SCARRecord, 
        context: Dict[str, Any]
    ) -> Tuple[bool, Any]:
        """Attempt recovery from SCAR state."""
        
        # Get strategies for this SCAR type
        strategies = self.strategies.get(scar.scar_type, [])
        
        # Check past successes for ordering
        suggestions = self.repository.get_recovery_suggestions(scar.scar_type)
        if suggestions:
            # Reorder strategies based on past success
            successful_names = [s["strategy"] for s in suggestions]
            strategies = sorted(
                strategies,
                key=lambda s: (
                    successful_names.index(s.__name__) 
                    if s.__name__ in successful_names 
                    else len(successful_names)
                )
            )
        
        # Try strategies in order
        for strategy in strategies:
            try:
                scar.recovery_attempted = True
                scar.recovery_strategy = strategy.__name__
                
                result = await strategy(scar, context)
                
                if result is not None:
                    scar.recovery_successful = True
                    scar.lessons_learned.append(
                        f"Recovered via {strategy.__name__}"
                    )
                    self.repository.store(scar)
                    return True, result
                    
            except Exception as e:
                scar.lessons_learned.append(
                    f"{strategy.__name__} failed: {str(e)[:100]}"
                )
        
        # All strategies failed
        scar.recovery_successful = False
        self.repository.store(scar)
        return False, None
    
    # Recovery strategy implementations
    async def _retry_with_extended_timeout(
        self, scar: SCARRecord, context: Dict
    ) -> Optional[Any]:
        """Retry with 2x timeout."""
        original_timeout = context.get("timeout", 30)
        context["timeout"] = original_timeout * 2
        # Re-execute with new timeout
        return await context["executor"](context)
    
    async def _switch_provider(
        self, scar: SCARRecord, context: Dict
    ) -> Optional[Any]:
        """Switch to backup provider."""
        failed_provider = context.get("provider")
        backup_providers = context.get("backup_providers", [])
        
        for backup in backup_providers:
            if backup != failed_provider:
                context["provider"] = backup
                return await context["executor"](context)
        
        return None
    
    async def _retry_with_backoff(
        self, scar: SCARRecord, context: Dict
    ) -> Optional[Any]:
        """Retry with exponential backoff."""
        max_retries = 3
        for attempt in range(max_retries):
            await asyncio.sleep(2 ** attempt)
            try:
                return await context["executor"](context)
            except Exception:
                continue
        return None
    
    async def _decompose_and_retry(
        self, scar: SCARRecord, context: Dict
    ) -> Optional[Any]:
        """Break task into smaller chunks."""
        if "decomposer" in context:
            subtasks = context["decomposer"](context["task"])
            results = []
            for subtask in subtasks:
                context["task"] = subtask
                result = await context["executor"](context)
                if result:
                    results.append(result)
            if results:
                return context.get("aggregator", lambda x: x)(results)
        return None
    
    async def _fallback_to_simpler_model(
        self, scar: SCARRecord, context: Dict
    ) -> Optional[Any]:
        """Use simpler/faster model."""
        fallback_models = {
            "gpt-4-turbo": "gpt-3.5-turbo",
            "claude-3-opus": "claude-3-sonnet",
            "gemini-1.5-pro": "gemini-1.5-flash"
        }
        current_model = context.get("model")
        if current_model in fallback_models:
            context["model"] = fallback_models[current_model]
            return await context["executor"](context)
        return None
    
    async def _relax_constraints(
        self, scar: SCARRecord, context: Dict
    ) -> Optional[Any]:
        """Relax validation constraints."""
        context["strict_validation"] = False
        return await context["executor"](context)
    
    async def _reduce_batch_size(
        self, scar: SCARRecord, context: Dict
    ) -> Optional[Any]:
        """Reduce batch size for resource errors."""
        current_batch = context.get("batch_size", 100)
        context["batch_size"] = current_batch // 2
        if context["batch_size"] > 0:
            return await context["executor"](context)
        return None
```

---

# 21. OPERATIONAL RUNBOOKS

## 21.1 System Initialization

```yaml
runbook: system_initialization
description: Cold boot GhostLink from kernel seed
steps:
  - name: Verify kernel integrity
    command: |
      sha256sum kernel.json
      # Expected: <known_hash>
    verify: hash matches manifest
    
  - name: Initialize database
    command: |
      psql -f schema/init.sql
      psql -f schema/seed_agents.sql
    verify: 64 agents created
    
  - name: Start pheromone service
    command: |
      systemctl start ghostlink-pheromones
    verify: service status active
    healthcheck: curl http://localhost:8001/health
    
  - name: Start DAK coordinator
    command: |
      wrangler dev --local
    verify: Durable Objects initialized
    healthcheck: curl http://localhost:8787/status
    
  - name: Initialize provider connections
    command: |
      python -m ghostlink.providers.healthcheck
    verify: ≥3 providers healthy
    
  - name: Run smoke test
    command: |
      python -m ghostlink.test.smoke
    verify: all assertions pass
    
  - name: Emit BOOT trace event
    automatic: true
    verify: event logged with kernel_hash
```

## 21.2 Incident Response

```yaml
runbook: incident_response
description: Handle production incidents
severity_levels:
  P1: System down, no queries processing
  P2: Degraded performance, partial functionality
  P3: Minor issues, workarounds available
  P4: Cosmetic/informational

procedures:
  P1_response:
    time_to_engage: 5 minutes
    steps:
      - Acknowledge incident in #ghostlink-incidents
      - Check provider health: `ghostlink status providers`
      - Check agent health: `ghostlink status agents`
      - If provider down:
          - Activate backup providers
          - Update routing to exclude failed provider
      - If agent failure cascade:
          - Identify failed agents: `ghostlink diagnose agents`
          - Isolate affected group
          - Reroute through healthy paths
      - If database issue:
          - Check connection pool: `ghostlink db status`
          - Restart connections if needed
          - Verify data integrity
      - Document timeline
      - Notify stakeholders
      
  P2_response:
    time_to_engage: 15 minutes
    steps:
      - Acknowledge incident
      - Identify degraded component
      - Apply rate limiting if load-related
      - Check SCAR repository for similar patterns
      - Apply suggested recovery strategy
      - Monitor for 15 minutes
      - Escalate to P1 if not resolved
      
  recovery_verification:
    steps:
      - Run smoke tests
      - Verify variance analysis quality
      - Check latency percentiles
      - Confirm no new SCARs generated
      - Clear incident status
```

## 21.3 Scaling Operations

```yaml
runbook: horizontal_scaling
description: Scale system capacity
triggers:
  - query_latency_p99 > 5000ms for 5 minutes
  - queue_depth > 1000
  - provider_error_rate > 10%

scale_up:
  steps:
    - name: Add worker capacity
      command: |
        wrangler deploy --env production --scale 2x
      verify: new workers accepting traffic
      
    - name: Increase provider rate limits
      command: |
        ghostlink config set rate_limit.openai 20
        ghostlink config set rate_limit.anthropic 15
      verify: config updated
      
    - name: Expand connection pools
      command: |
        ghostlink db pool --size 50
      verify: pool expanded
      
    - name: Enable caching tier
      command: |
        ghostlink cache enable --tier aggressive
      verify: cache hit rate > 0
      
scale_down:
  triggers:
    - query_latency_p99 < 500ms for 30 minutes
    - queue_depth < 100
    - cpu_utilization < 30%
  steps:
    - Reduce workers by 50%
    - Reset rate limits to baseline
    - Shrink connection pools
    - Disable aggressive caching
```

## 21.4 Backup and Recovery

```yaml
runbook: backup_and_recovery
description: Data protection procedures

backup_schedule:
  continuous:
    - Event log (append-only)
    - Audit trail (hash-chained)
  hourly:
    - Pheromone state snapshots
    - SCAR repository
  daily:
    - Full database backup
    - Configuration export
  weekly:
    - Cold storage archive
    - Integrity verification

recovery_procedures:
  point_in_time:
    description: Restore to specific timestamp
    steps:
      - Identify target timestamp
      - Stop all incoming queries
      - Restore database: `ghostlink db restore --timestamp <ts>`
      - Replay event log from timestamp
      - Rebuild pheromone state
      - Verify consistency
      - Resume operations
      
  disaster_recovery:
    description: Full system recovery
    rto: 4 hours
    rpo: 1 hour
    steps:
      - Provision new infrastructure
      - Restore from latest backup
      - Apply transaction log
      - Verify all 64 agents operational
      - Run comprehensive test suite
      - Redirect traffic
      - Monitor for 1 hour
```

## 21.5 Maintenance Windows

```yaml
runbook: maintenance_window
description: Scheduled maintenance procedures

pre_maintenance:
  t_minus_24h:
    - Notify users of scheduled maintenance
    - Verify backup completion
    - Stage deployment artifacts
  t_minus_1h:
    - Final backup
    - Verify rollback procedure
    - Alert on-call team
  t_minus_5m:
    - Enable maintenance mode
    - Drain active queries
    - Disable new query intake

during_maintenance:
  steps:
    - Execute planned changes
    - Run validation tests
    - Verify system health
    - Document any issues

post_maintenance:
  steps:
    - Disable maintenance mode
    - Resume query processing
    - Monitor for 30 minutes
    - Verify performance baselines
    - Send completion notification
    
rollback_triggers:
  - Any P1 issue during maintenance
  - Test suite failures > 5%
  - Latency increase > 200%
  - Error rate increase > 5%
```

---

# 22. MONITORING & OBSERVABILITY

## 22.1 Key Metrics

```yaml
metrics:
  latency:
    - cmfl_cycle_duration_ms:
        description: End-to-end CMFL cycle time
        percentiles: [p50, p90, p99]
        alert_threshold: p99 > 5000ms
    - provider_response_ms:
        description: Individual provider latency
        labels: [provider, model]
        alert_threshold: p99 > 10000ms
    - pipeline_stage_ms:
        description: Per-stage processing time
        labels: [stage]
        
  throughput:
    - queries_per_second:
        description: Query processing rate
        alert_threshold: < 10 for 5 minutes
    - variance_analyses_per_minute:
        description: Variance analysis completions
        
  errors:
    - error_rate:
        description: Percentage of failed queries
        alert_threshold: > 5%
    - scar_generation_rate:
        description: SCAR records per minute
        alert_threshold: > 10
    - provider_error_rate:
        labels: [provider]
        alert_threshold: > 10%
        
  resources:
    - memory_usage_bytes:
        alert_threshold: > 80% of limit
    - cpu_utilization:
        alert_threshold: > 90% for 5 minutes
    - connection_pool_utilization:
        alert_threshold: > 80%
        
  business:
    - variance_confidence_score:
        description: Mean confidence in variance analysis
        alert_threshold: < 0.7
    - consensus_rate:
        description: Percentage of queries achieving consensus
    - provider_diversity:
        description: Number of healthy providers
        alert_threshold: < 3
```

## 22.2 Alerting Rules

```yaml
alerts:
  critical:
    - name: SystemDown
      condition: queries_per_second == 0 for 2 minutes
      action: Page on-call immediately
      
    - name: AllProvidersUnhealthy
      condition: healthy_providers == 0
      action: Page on-call, activate emergency cache
      
    - name: DatabaseUnreachable
      condition: db_connection_errors > 10 per minute
      action: Page on-call, check infrastructure
      
  warning:
    - name: HighLatency
      condition: cmfl_cycle_duration_p99 > 5000ms for 5 minutes
      action: Notify team, check provider health
      
    - name: ElevatedErrorRate
      condition: error_rate > 5% for 5 minutes
      action: Notify team, check SCAR patterns
      
    - name: LowConfidence
      condition: variance_confidence_score < 0.5 for 10 minutes
      action: Notify team, investigate variance patterns
      
  info:
    - name: ProviderDegraded
      condition: provider_error_rate > 5% for provider
      action: Log, consider provider substitution
```

## 22.3 Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GHOSTLINK OPERATIONS DASHBOARD                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐ │
│  │   SYSTEM HEALTH     │  │   QUERY THROUGHPUT  │  │   ERROR RATE        │ │
│  │   ████████░░ 85%    │  │   ▄▄▄▄▄▄▄▄▄▄▄▄     │  │   ▁▁▂▁▁▁▁▁▁▁▁▁     │ │
│  │   64/64 agents      │  │   45 qps            │  │   0.8%              │ │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      PROVIDER STATUS                                 │   │
│  │  ✓ OpenAI GPT-4      ✓ Anthropic Claude    ✓ Google Gemini         │   │
│  │    p99: 2.1s           p99: 1.8s             p99: 2.4s              │   │
│  │  ✓ Mistral Large     ✓ OpenAI GPT-4o       ⚠ Anthropic Opus        │   │
│  │    p99: 1.5s           p99: 1.2s             p99: 8.5s (degraded)   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌───────────────────────────────┐  ┌───────────────────────────────────┐  │
│  │      CMFL CYCLE LATENCY       │  │       VARIANCE CONFIDENCE         │  │
│  │                               │  │                                   │  │
│  │   p50: 1,234ms               │  │   Mean: 0.82                      │  │
│  │   p90: 2,456ms               │  │   ▄▄▄▄▄▄▄▄████████████████       │  │
│  │   p99: 4,567ms               │  │   0.0            0.5           1.0│  │
│  │   ▄▄▄▄▄▄▄▆▆▆▆▆███████████   │  │                                   │  │
│  └───────────────────────────────┘  └───────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      RECENT SCAR EVENTS                              │   │
│  │  12:34:56  TIMEOUT      Provider: anthropic_opus    Recovered: ✓    │   │
│  │  12:33:21  VALIDATION   Pipeline: P-04             Recovered: ✓    │   │
│  │  12:31:45  NETWORK      Provider: google_gemini     Recovered: ✓    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*End of Part 5*
*Continue to Part 6: Advanced Topics & Research Directions*
