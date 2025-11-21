# GhostLink Computation Language Translator

A comprehensive translation system for converting code between multiple programming languages with syntax analysis, semantic preservation, and cross-language idiom mapping.

## Features

- **Multi-Language Support**: Supports 13+ programming languages
- **Automatic Language Detection**: Intelligent pattern-based detection with confidence scoring
- **Syntax Translation**: Converts language-specific syntax patterns
- **Type Mapping**: Maps type systems between languages
- **Indentation Adjustment**: Adjusts code style to target language conventions
- **Batch Processing**: Translate multiple code blocks efficiently
- **Pipeline Integration**: Seamlessly integrates with GhostLink's opcode system

## Supported Languages

- Python
- JavaScript / TypeScript
- Java
- C / C++
- Go
- Rust
- Ruby
- PHP
- Swift
- Kotlin
- C#

## Installation

The translator is included in the GhostLink package. No additional installation required.

```bash
pip install -e .
```

## Quick Start

### Basic Translation

```python
from ghostlink.translator import ComputationLanguageTranslator

translator = ComputationLanguageTranslator()

# Translate Python to JavaScript
python_code = """
def hello_world():
    print("Hello, World!")
    return True
"""

result = translator.translate(python_code, "javascript")
print(result['translated_code'])
```

### Language Detection

```python
from ghostlink.translator import detect_language

code = """
function helloWorld() {
    console.log("Hello!");
}
"""

language = detect_language(code)
print(f"Detected language: {language}")  # Output: javascript
```

### With Confidence Score

```python
from ghostlink.translator import ComputationLanguageTranslator

translator = ComputationLanguageTranslator()
lang, confidence = translator.detect_language_with_confidence(code)
print(f"Language: {lang.value}, Confidence: {confidence:.2%}")
```

## API Reference

### ComputationLanguageTranslator

Main class for language translation operations.

#### Methods

##### `detect_language(code: str) -> Language`

Detect the programming language from source code.

**Parameters:**
- `code`: Source code string

**Returns:**
- `Language` enum value

**Example:**
```python
translator = ComputationLanguageTranslator()
lang = translator.detect_language("def test(): pass")
print(lang)  # Language.PYTHON
```

##### `detect_language_with_confidence(code: str) -> Tuple[Language, float]`

Detect language with a confidence score.

**Parameters:**
- `code`: Source code string

**Returns:**
- Tuple of `(Language, confidence_score)` where confidence is 0.0-1.0

**Example:**
```python
lang, conf = translator.detect_language_with_confidence(code)
print(f"{lang.value}: {conf:.2%}")
```

##### `translate(source_code: str, target_language: str, source_language: Optional[str] = None) -> Dict[str, Any]`

Translate code from one language to another.

**Parameters:**
- `source_code`: Source code to translate
- `target_language`: Target language name (e.g., "python", "javascript")
- `source_language`: Optional source language (auto-detected if None)

**Returns:**
- Dictionary containing:
  - `success`: Boolean indicating success
  - `source_language`: Detected or specified source language
  - `target_language`: Target language
  - `source_code`: Original source code
  - `translated_code`: Translated code
  - `confidence`: Translation confidence score (0.0-1.0)
  - `warnings`: List of warning messages
  - `metadata`: Additional metadata

**Example:**
```python
result = translator.translate(
    "def add(a, b): return a + b",
    target_language="javascript"
)

if result['success']:
    print(result['translated_code'])
else:
    print(f"Error: {result['error']}")
```

##### `get_supported_languages() -> List[str]`

Get list of all supported programming languages.

**Returns:**
- List of language names

**Example:**
```python
languages = translator.get_supported_languages()
print(languages)  # ['python', 'javascript', 'java', ...]
```

##### `get_supported_translations() -> Dict[str, List[str]]`

Get dictionary of supported translation pairs.

**Returns:**
- Dictionary mapping source languages to list of target languages

**Example:**
```python
translations = translator.get_supported_translations()
for source, targets in translations.items():
    print(f"{source} can translate to: {', '.join(targets)}")
```

## Convenience Functions

### `detect_language(code: str) -> str`

Quick language detection function.

```python
from ghostlink.translator import detect_language

lang = detect_language("print('Hello')")
print(lang)  # 'python'
```

### `translate_code(source_code: str, target_language: str, source_language: Optional[str] = None) -> Dict[str, Any]`

Quick translation function.

```python
from ghostlink.translator import translate_code

result = translate_code(
    "console.log('Hello')",
    "python",
    source_language="javascript"
)
print(result['translated_code'])  # print('Hello')
```

### `get_supported_languages() -> List[str]`

Get list of supported languages.

```python
from ghostlink.translator import get_supported_languages

languages = get_supported_languages()
```

## GhostLink Pipeline Integration

The translator integrates with GhostLink's opcode system for pipeline orchestration.

### Registering Opcodes

```python
from ghostlink.translator import register_translator_opcodes

opcodes = register_translator_opcodes()
# Returns opcode definitions for pipeline integration
```

### Available Opcodes

- **0xT1 - DETECT_LANG**: Detect programming language
  - Args: `code -> language`
  - Effect: Detect programming language

- **0xT2 - TRANSLATE**: Translate between languages
  - Args: `code, target_lang -> translated_code`
  - Effect: Translate between languages

- **0xT3 - LIST_LANGS**: List supported languages
  - Args: `-> languages[]`
  - Effect: List supported languages

### Using in Tools Module

```python
from ghostlink.tools import get_translator, detect_language, translate_code

# Get translator instance
translator = get_translator()

# Use convenience functions
lang = detect_language(code)
result = translate_code(code, "python")
```

## Translation Examples

### Python to JavaScript

**Input (Python):**
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

**Output (JavaScript):**
```javascript
function fibonacci(n) {
  if (n <= 1) {
    return n
  }
  return fibonacci(n-1) + fibonacci(n-2)
}
```

### JavaScript to Python

**Input (JavaScript):**
```javascript
function greet(name) {
    console.log("Hello, " + name);
}
```

**Output (Python):**
```python
def greet(name):
    print("Hello, " + name)
```

### Python to Java

**Input (Python):**
```python
def calculate(x, y):
    print("Calculating...")
    return x + y
```

**Output (Java):**
```java
public void calculate(x, y) {
    System.out.println("Calculating...");
    return x + y
}
```

## Advanced Usage

### Batch Translation

```python
from ghostlink.translator import TranslationEngine, CodeBlock, Language

engine = TranslationEngine()

code_blocks = [
    CodeBlock(content="def func1(): pass", language=Language.PYTHON),
    CodeBlock(content="def func2(): pass", language=Language.PYTHON),
]

results = engine.translate_batch(code_blocks, Language.JAVASCRIPT)

for result in results:
    print(f"Translated: {result.translated_code}")
```

### Type Mapping

```python
from ghostlink.translator import TypeMapper, Language

# Map Python int to Java
java_type = TypeMapper.map_type('int', Language.PYTHON, Language.JAVA)
print(java_type)  # 'int'

# Map Python str to Java
java_type = TypeMapper.map_type('str', Language.PYTHON, Language.JAVA)
print(java_type)  # 'String'
```

### Custom Translation Patterns

The translation engine uses pattern-based translation. You can extend it by adding custom patterns:

```python
from ghostlink.translator import TranslationEngine, SyntaxPattern

engine = TranslationEngine()

# Add custom pattern
custom_pattern = SyntaxPattern(
    name="custom_loop",
    source_pattern=r'for\s+(\w+)\s+in\s+range\((.*?)\):',
    target_template=r'for (let \1 = 0; \1 < \2; \1++) {'
)

# Use in translation
# (Note: Pattern registration would need to be added to the engine)
```

## Error Handling

The translator handles errors gracefully and provides informative messages:

```python
result = translator.translate(code, "unsupported_language")

if not result['success']:
    print(f"Error: {result['error']}")
    print(f"Supported: {result['supported_languages']}")
```

## Warnings and Confidence

Translation results include warnings and confidence scores:

```python
result = translator.translate(code, "javascript")

print(f"Confidence: {result['confidence']:.2%}")
if result['warnings']:
    print("Warnings:")
    for warning in result['warnings']:
        print(f"  - {warning}")
```

## Limitations

- **Semantic Preservation**: The translator focuses on syntax conversion and may not preserve all semantic nuances
- **Library-Specific Code**: Code using language-specific libraries may not translate perfectly
- **Complex Patterns**: Very complex code patterns may require manual adjustment
- **Type Inference**: Some type mappings may be approximate
- **Idioms**: Language-specific idioms may translate literally rather than idiomatically

## Best Practices

1. **Review Translations**: Always review generated code for correctness
2. **Test Thoroughly**: Run tests on translated code
3. **Use for Reference**: Treat translations as a starting point, not final code
4. **Check Warnings**: Pay attention to warnings in translation results
5. **Specify Source Language**: For better accuracy, specify the source language explicitly
6. **Handle Edge Cases**: Add manual adjustments for language-specific features

## Contributing

To add support for a new language:

1. Add language to `Language` enum
2. Add detection patterns to `LanguageDetector.PATTERNS`
3. Add type mappings to `TypeMapper.TYPE_MAPS`
4. Add translation patterns to `TranslationEngine._init_patterns()`
5. Update tests in `tests/test_translator.py`

## Testing

Run the test suite:

```bash
# Run all translator tests
pytest tests/test_translator.py -v

# Run specific test class
pytest tests/test_translator.py::TestLanguageDetector -v

# Run with coverage
pytest tests/test_translator.py --cov=ghostlink.translator
```

## Performance

- Language detection: O(n) where n is code length
- Translation: O(n × p) where p is number of patterns
- Batch processing: Parallelizable for multiple code blocks

## License

Part of the GhostLink project. See main LICENSE file for details.

## Support

For issues, questions, or contributions:
- File issues on the GhostLink repository
- Check test cases for usage examples
- Review inline documentation in the source code

---

**Built for the GhostLink AI Ecosystem** 🧠⚡
