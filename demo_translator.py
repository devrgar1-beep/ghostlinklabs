#!/usr/bin/env python3
"""
GhostLink Computation Language Translator Demo

Demonstrates the capabilities of the translator with various examples.
"""

from ghostlink.translator import ComputationLanguageTranslator


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_language_detection():
    """Demonstrate language detection"""
    print_section("Language Detection Demo")
    
    translator = ComputationLanguageTranslator()
    
    examples = [
        ("Python", "def fibonacci(n):\n    return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"),
        ("JavaScript", "function greet(name) {\n    console.log(`Hello, ${name}`);\n}"),
        ("Java", "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}"),
        ("Go", "package main\n\nimport \"fmt\"\n\nfunc main() {\n    fmt.Println(\"Hello\")\n}"),
        ("Rust", "fn main() {\n    println!(\"Hello, world!\");\n}"),
    ]
    
    for expected, code in examples:
        detected, confidence = translator.detect_language_with_confidence(code)
        status = "✓" if detected.value == expected.lower() else "✗"
        print(f"\n{status} Expected: {expected:12} | Detected: {detected.value:12} | Confidence: {confidence:.1%}")
        print(f"   Code: {code[:50]}...")


def demo_translation(source_lang, target_lang, code, description):
    """Demonstrate a single translation"""
    translator = ComputationLanguageTranslator()
    
    print(f"\n{description}")
    print(f"  {source_lang.upper()} → {target_lang.upper()}")
    print("-" * 70)
    
    print(f"\nSource ({source_lang}):")
    print(code)
    
    result = translator.translate(code, target_lang, source_lang)
    
    if result['success']:
        print(f"\nTranslated ({target_lang}):")
        print(result['translated_code'])
        print(f"\nConfidence: {result['confidence']:.1%}")
        if result['warnings']:
            print("Warnings:")
            for warning in result['warnings']:
                print(f"  - {warning}")
    else:
        print(f"\n✗ Translation failed: {result.get('error', 'Unknown error')}")


def demo_translations():
    """Demonstrate various translations"""
    print_section("Code Translation Demo")
    
    # Python to JavaScript
    demo_translation(
        "python", "javascript",
        """def greet(name):
    print("Hello, " + name)
    if name:
        return True""",
        "Example 1: Simple Function"
    )
    
    # JavaScript to Python
    demo_translation(
        "javascript", "python",
        """function calculate(x, y) {
    console.log("Calculating...");
    const result = x + y;
    return result;
}""",
        "Example 2: Function with Variables"
    )
    
    # Python to Java
    demo_translation(
        "python", "java",
        """def process_data(items):
    print("Processing...")
    for item in items:
        print(item)""",
        "Example 3: Loop Processing"
    )
    
    # Python to Go
    demo_translation(
        "python", "go",
        """def fibonacci(n):
    if n <= 1:
        return n
    print("Computing fibonacci")""",
        "Example 4: Recursive Function"
    )


def demo_batch_translation():
    """Demonstrate batch translation"""
    print_section("Batch Translation Demo")
    
    from ghostlink.translator import TranslationEngine, CodeBlock, Language
    
    engine = TranslationEngine()
    
    code_blocks = [
        CodeBlock(content="def func1(): print('One')", language=Language.PYTHON),
        CodeBlock(content="def func2(): print('Two')", language=Language.PYTHON),
        CodeBlock(content="def func3(): print('Three')", language=Language.PYTHON),
    ]
    
    print("\nTranslating 3 Python functions to JavaScript...\n")
    results = engine.translate_batch(code_blocks, Language.JAVASCRIPT)
    
    for i, result in enumerate(results, 1):
        print(f"Function {i}:")
        print(f"  Source:     {result.source_code.strip()}")
        print(f"  Translated: {result.translated_code.strip()}")
        print(f"  Confidence: {result.confidence:.1%}\n")


def demo_supported_languages():
    """Show all supported languages"""
    print_section("Supported Languages")
    
    translator = ComputationLanguageTranslator()
    
    languages = translator.get_supported_languages()
    print(f"\nTotal Languages: {len(languages)}\n")
    
    # Print in columns
    cols = 3
    for i in range(0, len(languages), cols):
        row = languages[i:i+cols]
        print("  " + "".join(f"{lang:20}" for lang in row))
    
    print("\n\nSupported Translation Pairs:")
    translations = translator.get_supported_translations()
    for source, targets in sorted(translations.items()):
        print(f"  {source:12} → {', '.join(targets)}")


def demo_opcode_integration():
    """Demonstrate GhostLink opcode integration"""
    print_section("GhostLink Opcode Integration")
    
    from ghostlink.translator import register_translator_opcodes
    
    opcodes = register_translator_opcodes()
    
    print("\nRegistered Opcodes:\n")
    for opcode_id, opcode_data in sorted(opcodes.items()):
        print(f"  {opcode_id}: {opcode_data['name']}")
        print(f"    Args:   {opcode_data['args']}")
        print(f"    Effect: {opcode_data['effect']}")
        print()


def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("  GHOSTLINK COMPUTATION LANGUAGE TRANSLATOR")
    print("  Demonstration Suite")
    print("=" * 70)
    
    try:
        demo_language_detection()
        demo_translations()
        demo_batch_translation()
        demo_supported_languages()
        demo_opcode_integration()
        
        print("\n" + "=" * 70)
        print("  Demo Complete!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
