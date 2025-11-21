"""
GhostLink Computation Language Translator

A comprehensive translation system for converting code between multiple programming languages.
Supports syntax analysis, semantic preservation, and cross-language idiom mapping.

Supported Languages:
- Python
- JavaScript/TypeScript
- Java
- C/C++
- Go
- Rust
- Ruby
- PHP
- Swift
- Kotlin
- C#
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class Language(Enum):
    """Supported programming languages"""

    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    C = "c"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"
    RUBY = "ruby"
    PHP = "php"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    CSHARP = "csharp"
    UNKNOWN = "unknown"


@dataclass
class CodeBlock:
    """Represents a block of code with metadata"""

    content: str
    language: Language
    block_type: str = "generic"  # function, class, statement, etc.
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    """Result of a translation operation"""

    source_language: Language
    target_language: Language
    source_code: str
    translated_code: str
    confidence: float
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class LanguageDetector:
    """Detects programming language from source code"""

    # Language-specific patterns for detection
    PATTERNS = {
        Language.PYTHON: [
            r"^\s*def\s+\w+\s*\(",
            r"^\s*class\s+\w+.*:",
            r"^\s*import\s+\w+",
            r"^\s*from\s+\w+\s+import",
            r'if\s+__name__\s*==\s*["\']__main__["\']',
        ],
        Language.JAVASCRIPT: [
            r"^\s*function\s+\w+\s*\(",
            r"^\s*const\s+\w+\s*=",
            r"^\s*let\s+\w+\s*=",
            r"^\s*var\s+\w+\s*=",
            r"console\.log\(",
            r"=>",
        ],
        Language.TYPESCRIPT: [
            r":\s*\w+\s*=",
            r"interface\s+\w+",
            r"type\s+\w+\s*=",
            r"<\w+>",
            r"as\s+\w+",
        ],
        Language.JAVA: [
            r"^\s*public\s+class\s+\w+",
            r"^\s*private\s+\w+\s+\w+",
            r"^\s*protected\s+\w+",
            r"System\.out\.println",
            r"@Override",
        ],
        Language.C: [
            r"#include\s*<\w+\.h>",
            r"^\s*int\s+main\s*\(",
            r"printf\(",
            r"scanf\(",
            r"\*\w+\s*;",
        ],
        Language.CPP: [
            r"#include\s*<iostream>",
            r"std::",
            r"^\s*class\s+\w+\s*\{",
            r"cout\s*<<",
            r"cin\s*>>",
            r"namespace\s+\w+",
        ],
        Language.GO: [
            r"^\s*package\s+\w+",
            r"^\s*func\s+\w+\s*\(",
            r"^\s*import\s+\(",
            r":=",
            r"fmt\.Print",
        ],
        Language.RUST: [
            r"^\s*fn\s+\w+\s*\(",
            r"^\s*let\s+mut\s+\w+",
            r"^\s*impl\s+\w+",
            r"println!\(",
            r"&str",
            r"->\s*\w+",
        ],
        Language.RUBY: [
            r"^\s*def\s+\w+",
            r"^\s*class\s+\w+",
            r"^\s*module\s+\w+",
            r"puts\s+",
            r"\.each\s+do\s*\|",
            r"end\s*$",
        ],
        Language.PHP: [
            r"<\?php",
            r"\$\w+\s*=",
            r"^\s*function\s+\w+\s*\(",
            r"echo\s+",
            r"->\w+",
        ],
        Language.SWIFT: [
            r"^\s*func\s+\w+\s*\(",
            r"^\s*var\s+\w+:\s*\w+",
            r"^\s*let\s+\w+:\s*\w+",
            r"print\(",
            r"import\s+Foundation",
        ],
        Language.KOTLIN: [
            r"^\s*fun\s+\w+\s*\(",
            r"^\s*val\s+\w+",
            r"^\s*var\s+\w+",
            r"println\(",
            r":\s*\w+\?",
        ],
        Language.CSHARP: [
            r"^\s*using\s+\w+;",
            r"^\s*namespace\s+\w+",
            r"^\s*public\s+class\s+\w+",
            r"Console\.WriteLine",
            r"^\s*private\s+\w+\s+\w+",
        ],
    }

    @classmethod
    def detect(cls, code: str) -> Language:
        """
        Detect the programming language from source code.

        Args:
            code: Source code string

        Returns:
            Detected Language enum value
        """
        if not code or not code.strip():
            return Language.UNKNOWN

        # Count pattern matches for each language
        scores: Dict[Language, int] = {}

        for language, patterns in cls.PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, code, re.MULTILINE):
                    score += 1
            if score > 0:
                scores[language] = score

        if not scores:
            return Language.UNKNOWN

        # Return language with highest score
        return max(scores.items(), key=lambda x: x[1])[0]

    @classmethod
    def detect_with_confidence(cls, code: str) -> Tuple[Language, float]:
        """
        Detect language with confidence score.

        Args:
            code: Source code string

        Returns:
            Tuple of (Language, confidence_score)
        """
        if not code or not code.strip():
            return Language.UNKNOWN, 0.0

        scores: Dict[Language, int] = {}

        for language, patterns in cls.PATTERNS.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, code, re.MULTILINE))
                score += matches
            if score > 0:
                scores[language] = score

        if not scores:
            return Language.UNKNOWN, 0.0

        detected_lang = max(scores.items(), key=lambda x: x[1])[0]

        # Calculate confidence based on the score relative to pattern count
        # A reasonable heuristic: confidence increases with more pattern matches
        # Maximum expected matches per pattern is ~2-3 for typical code
        max_patterns = len(cls.PATTERNS[detected_lang])
        expected_max_score = max_patterns * 2  # Assume ~2 matches per pattern for strong confidence
        confidence = min(scores[detected_lang] / expected_max_score, 1.0)

        return detected_lang, confidence


class TypeMapper:
    """Maps types between different programming languages"""

    # Type mapping matrix: source_lang -> target_lang -> type_map
    TYPE_MAPS = {
        Language.PYTHON: {
            Language.JAVA: {
                "int": "int",
                "float": "double",
                "str": "String",
                "bool": "boolean",
                "list": "List",
                "dict": "Map",
                "None": "null",
            },
            Language.JAVASCRIPT: {
                "int": "number",
                "float": "number",
                "str": "string",
                "bool": "boolean",
                "list": "Array",
                "dict": "Object",
                "None": "null",
            },
            Language.GO: {
                "int": "int",
                "float": "float64",
                "str": "string",
                "bool": "bool",
                "list": "[]interface{}",
                "dict": "map[string]interface{}",
                "None": "nil",
            },
            Language.RUST: {
                "int": "i32",
                "float": "f64",
                "str": "String",
                "bool": "bool",
                "list": "Vec",
                "dict": "HashMap",
                "None": "None",
            },
        },
        # Add reverse mappings and other combinations as needed
    }

    @classmethod
    def map_type(cls, type_name: str, source_lang: Language, target_lang: Language) -> str:
        """
        Map a type from source language to target language.

        Args:
            type_name: Type name in source language
            source_lang: Source language
            target_lang: Target language

        Returns:
            Mapped type name in target language
        """
        if source_lang not in cls.TYPE_MAPS:
            return type_name

        if target_lang not in cls.TYPE_MAPS[source_lang]:
            return type_name

        return cls.TYPE_MAPS[source_lang][target_lang].get(type_name, type_name)


class SyntaxPattern:
    """Represents a syntax pattern for translation"""

    def __init__(self, name: str, source_pattern: str, target_template: str):
        self.name = name
        self.source_pattern = re.compile(source_pattern, re.MULTILINE)
        self.target_template = target_template

    def match(self, code: str) -> Optional[re.Match]:
        """Check if pattern matches the code"""
        return self.source_pattern.search(code)

    def transform(self, code: str) -> str:
        """Transform code using this pattern"""
        return self.source_pattern.sub(self.target_template, code)


class TranslationEngine:
    """Core engine for translating between programming languages"""

    def __init__(self):
        self.detector = LanguageDetector()
        self.type_mapper = TypeMapper()
        self._init_patterns()

    def _init_patterns(self):
        """Initialize translation patterns"""
        # Python to JavaScript patterns
        self.patterns: Dict[Tuple[Language, Language], List[SyntaxPattern]] = {
            (Language.PYTHON, Language.JAVASCRIPT): [
                SyntaxPattern("function_def", r"def\s+(\w+)\s*\((.*?)\)\s*:", r"function \1(\2) {"),
                SyntaxPattern("print", r"print\((.*?)\)", r"console.log(\1)"),
                SyntaxPattern("if_statement", r"if\s+(.*?)\s*:", r"if (\1) {"),
            ],
            (Language.PYTHON, Language.JAVA): [
                SyntaxPattern(
                    "function_def", r"def\s+(\w+)\s*\((.*?)\)\s*:", r"public void \1(\2) {"
                ),
                SyntaxPattern("print", r"print\((.*?)\)", r"System.out.println(\1);"),
            ],
            (Language.PYTHON, Language.GO): [
                SyntaxPattern("function_def", r"def\s+(\w+)\s*\((.*?)\)\s*:", r"func \1(\2) {"),
                SyntaxPattern("print", r"print\((.*?)\)", r"fmt.Println(\1)"),
            ],
            (Language.JAVASCRIPT, Language.PYTHON): [
                SyntaxPattern("function_def", r"function\s+(\w+)\s*\((.*?)\)\s*\{", r"def \1(\2):"),
                SyntaxPattern("console_log", r"console\.log\((.*?)\)", r"print(\1)"),
                SyntaxPattern("const", r"const\s+(\w+)\s*=", r"\1 ="),
            ],
        }

    def translate(
        self,
        source_code: str,
        source_lang: Optional[Language] = None,
        target_lang: Language = Language.PYTHON,
    ) -> TranslationResult:
        """
        Translate source code from one language to another.

        Args:
            source_code: Source code to translate
            source_lang: Source language (auto-detected if None)
            target_lang: Target language

        Returns:
            TranslationResult with translated code and metadata
        """
        warnings = []

        # Detect source language if not provided
        if source_lang is None:
            source_lang, confidence = self.detector.detect_with_confidence(source_code)
            if source_lang == Language.UNKNOWN:
                warnings.append("Could not detect source language")
                return TranslationResult(
                    source_language=source_lang,
                    target_language=target_lang,
                    source_code=source_code,
                    translated_code=source_code,
                    confidence=0.0,
                    warnings=warnings,
                )
        else:
            confidence = 1.0

        # If source and target are the same, return as-is
        if source_lang == target_lang:
            return TranslationResult(
                source_language=source_lang,
                target_language=target_lang,
                source_code=source_code,
                translated_code=source_code,
                confidence=1.0,
                warnings=["Source and target languages are the same"],
            )

        # Apply translation patterns
        translated_code = source_code
        pattern_key = (source_lang, target_lang)

        if pattern_key in self.patterns:
            for pattern in self.patterns[pattern_key]:
                translated_code = pattern.transform(translated_code)
        else:
            warnings.append(
                f"No direct translation patterns from {source_lang.value} to {target_lang.value}"
            )
            # Return original with warning
            return TranslationResult(
                source_language=source_lang,
                target_language=target_lang,
                source_code=source_code,
                translated_code=source_code,
                confidence=0.0,
                warnings=warnings,
            )

        # Adjust indentation for target language
        translated_code = self._adjust_indentation(translated_code, source_lang, target_lang)

        return TranslationResult(
            source_language=source_lang,
            target_language=target_lang,
            source_code=source_code,
            translated_code=translated_code,
            confidence=confidence * 0.8,  # Reduce confidence due to translation
            warnings=warnings,
            metadata={
                "patterns_applied": len(self.patterns.get(pattern_key, [])),
            },
        )

    def _adjust_indentation(self, code: str, source_lang: Language, target_lang: Language) -> str:
        """
        Adjust code indentation based on target language conventions.

        Args:
            code: Code to adjust
            source_lang: Source language
            target_lang: Target language

        Returns:
            Code with adjusted indentation
        """
        # Python uses 4 spaces, JavaScript uses 2 spaces
        indentation_map = {
            Language.PYTHON: 4,
            Language.JAVASCRIPT: 2,
            Language.TYPESCRIPT: 2,
            Language.JAVA: 4,
            Language.C: 2,
            Language.CPP: 2,
            Language.GO: 1,  # tabs
            Language.RUST: 4,
            Language.RUBY: 2,
            Language.PHP: 4,
            Language.SWIFT: 4,
            Language.KOTLIN: 4,
            Language.CSHARP: 4,
        }

        source_indent = indentation_map.get(source_lang, 4)
        target_indent = indentation_map.get(target_lang, 4)

        if source_indent == target_indent:
            return code

        # Simple indentation adjustment (more sophisticated logic could be added)
        lines = code.split("\n")
        adjusted_lines = []

        for line in lines:
            # Count leading spaces
            leading_spaces = len(line) - len(line.lstrip(" "))
            if leading_spaces > 0:
                indent_level = leading_spaces // source_indent
                new_indent = " " * (indent_level * target_indent)
                adjusted_lines.append(new_indent + line.lstrip(" "))
            else:
                adjusted_lines.append(line)

        return "\n".join(adjusted_lines)

    def translate_batch(
        self, code_blocks: List[CodeBlock], target_lang: Language
    ) -> List[TranslationResult]:
        """
        Translate multiple code blocks.

        Args:
            code_blocks: List of code blocks to translate
            target_lang: Target language

        Returns:
            List of translation results
        """
        results = []
        for block in code_blocks:
            result = self.translate(
                block.content, source_lang=block.language, target_lang=target_lang
            )
            results.append(result)
        return results


class ComputationLanguageTranslator:
    """
    Main interface for the GhostLink Computation Language Translator.

    Provides high-level API for language detection and translation.
    """

    def __init__(self):
        self.engine = TranslationEngine()
        self.detector = LanguageDetector()

    def detect_language(self, code: str) -> Language:
        """Detect programming language from code."""
        return self.detector.detect(code)

    def detect_language_with_confidence(self, code: str) -> Tuple[Language, float]:
        """Detect language with confidence score."""
        return self.detector.detect_with_confidence(code)

    def translate(
        self, source_code: str, target_language: str, source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate code from one language to another.

        Args:
            source_code: Source code to translate
            target_language: Target language name (e.g., "python", "javascript")
            source_language: Source language name (auto-detected if None)

        Returns:
            Dictionary with translation results
        """
        # Convert string language names to enum
        try:
            target_lang = Language(target_language.lower())
        except ValueError:
            return {
                "success": False,
                "error": f"Unsupported target language: {target_language}",
                "supported_languages": [
                    lang.value for lang in Language if lang != Language.UNKNOWN
                ],
            }

        source_lang = None
        if source_language:
            try:
                source_lang = Language(source_language.lower())
            except ValueError:
                return {
                    "success": False,
                    "error": f"Unsupported source language: {source_language}",
                    "supported_languages": [
                        lang.value for lang in Language if lang != Language.UNKNOWN
                    ],
                }

        # Perform translation
        result = self.engine.translate(source_code, source_lang, target_lang)

        return {
            "success": True,
            "source_language": result.source_language.value,
            "target_language": result.target_language.value,
            "source_code": result.source_code,
            "translated_code": result.translated_code,
            "confidence": result.confidence,
            "warnings": result.warnings,
            "metadata": result.metadata,
        }

    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return [lang.value for lang in Language if lang != Language.UNKNOWN]

    def get_supported_translations(self) -> Dict[str, List[str]]:
        """Get dictionary of supported translation pairs."""
        translations = {}
        for source, target in self.engine.patterns.keys():
            if source.value not in translations:
                translations[source.value] = []
            translations[source.value].append(target.value)
        return translations


# Convenience functions for direct use
def detect_language(code: str) -> str:
    """Detect programming language from code."""
    translator = ComputationLanguageTranslator()
    lang = translator.detect_language(code)
    return lang.value


def translate_code(
    source_code: str, target_language: str, source_language: Optional[str] = None
) -> Dict[str, Any]:
    """Translate code from one language to another."""
    translator = ComputationLanguageTranslator()
    return translator.translate(source_code, target_language, source_language)


def get_supported_languages() -> List[str]:
    """Get list of supported programming languages."""
    translator = ComputationLanguageTranslator()
    return translator.get_supported_languages()


# Integration with GhostLink pipeline
def register_translator_opcodes() -> Dict[str, Any]:
    """
    Register translator opcodes with GhostLink opcode system.

    Returns:
        Dictionary of translator opcodes for pipeline integration
    """
    return {
        "0xT1": {
            "name": "DETECT_LANG",
            "args": "code -> language",
            "effect": "detect programming language",
            "handler": detect_language,
        },
        "0xT2": {
            "name": "TRANSLATE",
            "args": "code,target_lang -> translated_code",
            "effect": "translate between languages",
            "handler": translate_code,
        },
        "0xT3": {
            "name": "LIST_LANGS",
            "args": "-> languages[]",
            "effect": "list supported languages",
            "handler": get_supported_languages,
        },
    }


if __name__ == "__main__":
    # Example usage
    translator = ComputationLanguageTranslator()

    # Example 1: Python to JavaScript
    python_code = """
def hello_world():
    print("Hello, World!")
    return True
"""

    result = translator.translate(python_code, "javascript")
    print("Python to JavaScript:")
    print(f"Success: {result['success']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Translated code:\n{result['translated_code']}")
    print()

    # Example 2: Language detection
    lang, confidence = translator.detect_language_with_confidence(python_code)
    print(f"Detected language: {lang.value} (confidence: {confidence})")
    print()

    # Example 3: List supported languages
    print("Supported languages:")
    for lang in translator.get_supported_languages():
        print(f"  - {lang}")
