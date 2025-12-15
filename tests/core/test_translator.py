"""Test the Computation Language Translator"""

import asyncio

from ghostlink.translator import (
    LanguageType,
    TranslationContext,
    get_translator,
    translate_code,
    translate_math,
)


async def test_language_translation():
    """Test programming language translation."""
    print("Testing Language Translation...")

    # Test Python to JavaScript
    python_code = """
def greet(name):
    print(f"Hello, {name}!")

greet("World")
"""

    context = TranslationContext(
        source_language=LanguageType.PYTHON, target_language=LanguageType.JAVASCRIPT
    )

    translator = get_translator()
    result = translator.translate(python_code, context)

    print(f"Original Python:\n{result.original}")
    print(f"Translated JavaScript:\n{result.translated}")
    print(f"Confidence: {result.confidence}")
    print()


async def test_math_translation():
    """Test mathematical notation translation."""
    print("Testing Mathematical Translation...")

    latex_math = r"\sum_{i=1}^{n} x_i = \alpha + \beta"

    result = translate_math(latex_math, "latex", "ascii")

    print(f"Original LaTeX: {result.original}")
    print(f"ASCII Math: {result.translated}")
    print(f"Confidence: {result.confidence}")
    print()


async def test_auto_detection():
    """Test automatic language detection and translation."""
    print("Testing Auto-Detection...")

    js_code = """
function calculate(x, y) {
    const result = x + y;
    console.log(result);
    return result;
}
"""

    translator = get_translator()
    result = translator.translate(js_code, TranslationContext())

    print(f"Original JS:\n{result.original}")
    print(f"Auto-translated:\n{result.translated}")
    print(f"Confidence: {result.confidence}")
    print()


async def test_convenience_functions():
    """Test convenience functions."""
    print("Testing Convenience Functions...")

    # Test translate_code
    result = translate_code("print('Hello')", "python", "javascript")
    print(f"Convenience translation: {result.translated}")

    # Test translate_math
    result = translate_math(r"\pi \approx 3.14", "latex", "unicode")
    print(f"Math translation: {result.translated}")
    print()


async def main():
    """Run all translator tests."""
    print("🧠 GhostLink Computation Language Translator Tests")
    print("=" * 50)

    try:
        await test_language_translation()
        await test_math_translation()
        await test_auto_detection()
        await test_convenience_functions()

        print("✅ All translator tests completed successfully!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
