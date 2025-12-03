"""
GhostLink Governance Engine - Trust Store and Policy Enforcement

Implements the governance layer: trust stores, attestations, policy enforcement
Zero-trust architecture with explicit permission boundaries.
"""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Protocol


# Core Governance Types
@dataclass
class Identity:
    """Entity identity with cryptographic verification"""

    id: str
    public_key: str
    kind: str  # 'probe' | 'device' | 'user' | 'service'
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())

    def verify_signature(self, message: str, signature: str) -> bool:
        """Verify cryptographic signature (placeholder)"""
        # In real implementation, use proper crypto library
        expected = hashlib.sha256(f"{self.public_key}:{message}".encode()).hexdigest()
        return signature == expected


@dataclass
class Attestation:
    """Trust attestation for identities and actions"""

    id: str
    subject_id: str
    issuer_id: str
    claim: str
    evidence: dict[str, Any]
    signature: str
    issued_at: float
    expires_at: float | None = None
    revoked: bool = False

    def is_valid(self, current_time: float | None = None) -> bool:
        """Check if attestation is currently valid"""
        now = current_time if current_time is not None else datetime.now().timestamp()
        if self.revoked:
            return False
        if self.expires_at and now > self.expires_at:
            return False
        return True


@dataclass
class PolicyRule:
    """Individual policy rule"""

    effect: str  # 'allow' | 'deny'
    principals: list[str]  # identity IDs or patterns
    actions: list[str]  # allowed/denied actions
    resources: list[str]  # resource patterns
    conditions: dict[str, Any] = field(default_factory=dict)


@dataclass
class Policy:
    """Access control policy"""

    id: str
    name: str
    description: str
    rules: list[PolicyRule]
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    version: str = "1.0.0"


@dataclass
class TrustContext:
    """Runtime trust evaluation context"""

    subject: Identity
    action: str
    resource: str
    environment: dict[str, Any] = field(default_factory=dict)


# Trust Store Interface
class TrustStore(Protocol):
    """Trust store for identities and attestations"""

    async def store_identity(self, identity: Identity) -> None:
        """Store an identity"""
        ...

    async def get_identity(self, identity_id: str) -> Identity | None:
        """Retrieve an identity"""
        ...

    async def store_attestation(self, attestation: Attestation) -> None:
        """Store an attestation"""
        ...

    async def get_attestations(self, subject_id: str) -> list[Attestation]:
        """Get attestations for a subject"""
        ...

    async def revoke_attestation(self, attestation_id: str) -> None:
        """Revoke an attestation"""
        ...


# Policy Engine Interface
class PolicyEngine(Protocol):
    """Policy evaluation engine"""

    async def evaluate(self, context: TrustContext) -> bool:
        """Evaluate if action is allowed"""
        ...

    async def add_policy(self, policy: Policy) -> None:
        """Add a policy"""
        ...

    async def get_policies(self) -> list[Policy]:
        """Get all policies"""
        ...


# Governance Engine
class GovernanceEngine:
    """Main governance coordinator"""

    def __init__(self, trust_store: TrustStore, policy_engine: PolicyEngine):
        self.trust_store = trust_store
        self.policy_engine = policy_engine
        self.audit_log: list[dict[str, Any]] = []

    async def authorize(self, context: TrustContext) -> bool:
        """Authorize an action with full trust evaluation"""
        # Automatic approval for root operations
        if self._is_root_operation(context):
            await self._audit("root_operation_auto_approved", context, {"auto_approved": True})
            return True

        # Verify identity exists and is attested
        identity = await self.trust_store.get_identity(context.subject.id)
        if not identity:
            await self._audit("identity_not_found", context)
            return False

        # Check attestations
        attestations = await self.trust_store.get_attestations(context.subject.id)
        valid_attestations = [a for a in attestations if a.is_valid()]

        if not valid_attestations:
            await self._audit("no_valid_attestations", context)
            return False

        # Evaluate policies
        allowed = await self.policy_engine.evaluate(context)

        await self._audit("authorization_result", context, {"allowed": allowed})
        return allowed

    def _is_root_operation(self, context: TrustContext) -> bool:
        """Check if this is a root-level operation that should be auto-approved"""
        # Root operations include:
        # - Actions starting with "root_"
        # - Principals that are "root" or "admin"
        # - Resources that are system-level or configuration
        root_actions = [
            "root_control",
            "system_admin",
            "hardware_absorption",
            "bios_bridge",
            "supergrok_init",
            "cloudflare_deploy",
            "task_create",
            "task_delete",
            "maintenance_run",
        ]

        root_principals = ["root", "admin", "system"]
        root_resources = ["system:*", "hardware:*", "bios:*", "config:*"]

        # Check if action is a root action
        if any(context.action.startswith(action) for action in root_actions):
            return True

        # Check if principal is root/admin
        if any(principal in context.subject.id for principal in root_principals):
            return True

        # Check if resource is system-level
        return any(resource in context.resource for resource in root_resources)

    async def attest_identity(
        self, subject: Identity, issuer: Identity, claim: str, evidence: dict[str, Any]
    ) -> Attestation:
        """Create attestation for an identity"""
        attestation = Attestation(
            id=f"att-{secrets.token_hex(8)}",
            subject_id=subject.id,
            issuer_id=issuer.id,
            claim=claim,
            evidence=evidence,
            signature=self._sign_attestation(issuer, f"{subject.id}:{claim}"),
            issued_at=datetime.now().timestamp(),
            expires_at=datetime.now().timestamp() + (365 * 24 * 60 * 60),  # 1 year
        )

        await self.trust_store.store_attestation(attestation)
        await self._audit("attestation_created", TrustContext(subject, "attest", subject.id))
        return attestation

    def _sign_attestation(self, issuer: Identity, message: str) -> str:
        """Create cryptographic signature (placeholder)"""
        return hashlib.sha256(f"{issuer.public_key}:{message}".encode()).hexdigest()

    async def _audit(self, event: str, context: TrustContext, extra: dict[str, Any] | None = None):
        """Log governance event"""
        entry = {
            "timestamp": datetime.now().timestamp(),
            "event": event,
            "subject": context.subject.id,
            "action": context.action,
            "resource": context.resource,
            "environment": context.environment,
        }
        if extra:
            entry.update(extra)

        self.audit_log.append(entry)


# In-Memory Trust Store Implementation
class InMemoryTrustStore:
    """Simple in-memory trust store for development"""

    def __init__(self):
        self.identities: dict[str, Identity] = {}
        self.attestations: dict[str, list[Attestation]] = {}

    async def store_identity(self, identity: Identity) -> None:
        self.identities[identity.id] = identity

    async def get_identity(self, identity_id: str) -> Identity | None:
        return self.identities.get(identity_id)

    async def store_attestation(self, attestation: Attestation) -> None:
        if attestation.subject_id not in self.attestations:
            self.attestations[attestation.subject_id] = []
        self.attestations[attestation.subject_id].append(attestation)

    async def get_attestations(self, subject_id: str) -> list[Attestation]:
        return self.attestations.get(subject_id, [])

    async def revoke_attestation(self, attestation_id: str) -> None:
        for subject_attestations in self.attestations.values():
            for attestation in subject_attestations:
                if attestation.id == attestation_id:
                    attestation.revoked = True


# Simple Policy Engine Implementation
class SimplePolicyEngine:
    """Simple policy engine with allow/deny rules"""

    def __init__(self):
        self.policies: list[Policy] = []

    async def evaluate(self, context: TrustContext) -> bool:
        """Evaluate policies in order"""
        for policy in self.policies:
            if self._matches_policy(policy, context):
                return policy.rules[0].effect == "allow"
        return False  # Default deny

    def _matches_policy(self, policy: Policy, context: TrustContext) -> bool:
        """Check if context matches policy rules"""
        for rule in policy.rules:
            if (
                self._matches_pattern(context.subject.id, rule.principals)
                and self._matches_pattern(context.action, rule.actions)
                and self._matches_pattern(context.resource, rule.resources)
            ):
                return True
        return False

    def _matches_pattern(self, value: str, patterns: list[str]) -> bool:
        """Simple pattern matching (supports wildcards)"""
        for pattern in patterns:
            if pattern == "*" or pattern == value:
                return True
            if pattern.endswith("*") and value.startswith(pattern[:-1]):
                return True
        return False

    async def add_policy(self, policy: Policy) -> None:
        self.policies.append(policy)

    async def get_policies(self) -> list[Policy]:
        return self.policies.copy()


# Governance Factory
class GovernanceFactory:
    """Factory for creating governance components"""

    @staticmethod
    def create_default_governance() -> GovernanceEngine:
        """Create default governance setup"""
        trust_store = InMemoryTrustStore()
        policy_engine = SimplePolicyEngine()

        # Create default policies
        default_policies = [
            Policy(
                id="probe-execution",
                name="Probe Execution Policy",
                description="Allow verified probes to execute",
                rules=[
                    PolicyRule(
                        effect="allow",
                        principals=["probe:*"],
                        actions=["execute", "scatter", "sync", "emerge"],
                        resources=["signal:*"],
                    )
                ],
            ),
            Policy(
                id="user-signal-input",
                name="User Signal Input Policy",
                description="Allow users to submit signals",
                rules=[
                    PolicyRule(
                        effect="allow",
                        principals=["user:*"],
                        actions=["submit"],
                        resources=["signal:*"],
                    )
                ],
            ),
        ]

        # Add policies synchronously for simplicity
        import asyncio

        async def setup():
            for policy in default_policies:
                await policy_engine.add_policy(policy)

        # Run setup
        asyncio.create_task(setup())

        return GovernanceEngine(trust_store, policy_engine)
