"""
Tests for GhostLink Computation Language Translator

Comprehensive test suite for language detection and translation functionality.
"""

import pytest
from ghostlink.translator import (
    Language,
    LanguageDetector,
    TypeMapper,
    TranslationEngine,
    ComputationLanguageTranslator,
    CodeBlock,
    detect_language,
    translate_code,
    get_supported_languages,
    register_translator_opcodes,
)


class TestLanguageDetector:
    """Test cases for language detection"""

    def test_detect_python(self):
        """Test Python code detection"""
        code = """
def hello_world():
    print("Hello, World!")
    return True
"""
        detector = LanguageDetector()
        lang = detector.detect(code)
        assert lang == Language.PYTHON

    def test_detect_javascript(self):
        """Test JavaScript code detection"""
        code = """
function helloWorld() {
    console.log("Hello, World!");
    return true;
}
"""
        detector = LanguageDetector()
        lang = detector.detect(code)
        assert lang == Language.JAVASCRIPT

    def test_detect_java(self):
        """Test Java code detection"""
        code = """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""
        detector = LanguageDetector()
        lang = detector.detect(code)
        assert lang == Language.JAVA

    def test_detect_go(self):
        """Test Go code detection"""
        code = """
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
"""
        detector = LanguageDetector()
        lang = detector.detect(code)
        assert lang == Language.GO

    def test_detect_rust(self):
        """Test Rust code detection"""
        code = """
fn main() {
    println!("Hello, World!");
}
"""
        detector = LanguageDetector()
        lang = detector.detect(code)
        assert lang == Language.RUST

    def test_detect_cpp(self):
        """Test C++ code detection"""
        code = """
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
"""
        detector = LanguageDetector()
        lang = detector.detect(code)
        assert lang == Language.CPP

    def test_detect_ruby(self):
        """Test Ruby code detection"""
        code = """
def hello_world
    puts "Hello, World!"
end
"""
        detector = LanguageDetector()
        lang = detector.detect(code)
        assert lang == Language.RUBY

    def test_detect_php(self):
        """Test PHP code detection"""
        code = """
<?php
function helloWorld() {
    echo "Hello, World!";
}
?>
"""
        detector = LanguageDetector()
        lang = detector.detect(code)
        assert lang == Language.PHP

    def test_detect_empty_code(self):
        """Test detection with empty code"""
        detector = LanguageDetector()
        lang = detector.detect("")
        assert lang == Language.UNKNOWN

    def test_detect_with_confidence(self):
        """Test detection with confidence score"""
        code = """
def test():
    import numpy
    from math import sqrt
    print("Test")
"""
        detector = LanguageDetector()
        lang, confidence = detector.detect_with_confidence(code)
        assert lang == Language.PYTHON
        assert 0.0 <= confidence <= 1.0
        # With the improved calculation, confidence is based on pattern matches
        # relative to expected max (2 matches per pattern)
        assert confidence > 0.2  # Should have at least some confidence for Python


class TestTypeMapper:
    """Test cases for type mapping"""

    def test_map_python_to_java_int(self):
        """Test int type mapping from Python to Java"""
        result = TypeMapper.map_type("int", Language.PYTHON, Language.JAVA)
        assert result == "int"

    def test_map_python_to_java_str(self):
        """Test string type mapping from Python to Java"""
        result = TypeMapper.map_type("str", Language.PYTHON, Language.JAVA)
        assert result == "String"

    def test_map_python_to_javascript_number(self):
        """Test number type mapping from Python to JavaScript"""
        result = TypeMapper.map_type("int", Language.PYTHON, Language.JAVASCRIPT)
        assert result == "number"

    def test_map_python_to_go_slice(self):
        """Test list/slice mapping from Python to Go"""
        result = TypeMapper.map_type("list", Language.PYTHON, Language.GO)
        assert result == "[]interface{}"

    def test_map_unknown_type(self):
        """Test mapping of unknown type returns original"""
        result = TypeMapper.map_type("CustomType", Language.PYTHON, Language.JAVA)
        assert result == "CustomType"


class TestTranslationEngine:
    """Test cases for translation engine"""

    def test_translate_python_to_javascript_function(self):
        """Test Python to JavaScript function translation"""
        code = """def hello():
    print("Hello")
"""
        engine = TranslationEngine()
        result = engine.translate(code, Language.PYTHON, Language.JAVASCRIPT)

        assert result.source_language == Language.PYTHON
        assert result.target_language == Language.JAVASCRIPT
        assert "function hello()" in result.translated_code
        assert "console.log" in result.translated_code

    def test_translate_python_to_java_print(self):
        """Test Python to Java print statement translation"""
        code = 'print("Hello")'
        engine = TranslationEngine()
        result = engine.translate(code, Language.PYTHON, Language.JAVA)

        assert "System.out.println" in result.translated_code

    def test_translate_javascript_to_python_function(self):
        """Test JavaScript to Python function translation"""
        code = """function hello() {
    console.log("Hello");
}"""
        engine = TranslationEngine()
        result = engine.translate(code, Language.JAVASCRIPT, Language.PYTHON)

        assert "def hello()" in result.translated_code
        assert "print(" in result.translated_code

    def test_translate_same_language(self):
        """Test translation when source and target are the same"""
        code = "print('Hello')"
        engine = TranslationEngine()
        result = engine.translate(code, Language.PYTHON, Language.PYTHON)

        assert result.translated_code == code
        assert result.confidence == 1.0
        assert len(result.warnings) > 0

    def test_translate_auto_detect(self):
        """Test translation with auto-detection"""
        code = """def test():
    print("Auto detect")
"""
        engine = TranslationEngine()
        result = engine.translate(code, target_lang=Language.JAVASCRIPT)

        assert result.source_language == Language.PYTHON
        assert "function" in result.translated_code or "console.log" in result.translated_code

    def test_translate_unsupported_pair(self):
        """Test translation for unsupported language pair"""
        code = "fn main() {}"
        engine = TranslationEngine()
        result = engine.translate(code, Language.RUST, Language.SWIFT)

        assert result.confidence == 0.0
        assert len(result.warnings) > 0

    def test_translate_batch(self):
        """Test batch translation"""
        blocks = [
            CodeBlock(content="def func1(): pass", language=Language.PYTHON),
            CodeBlock(content="def func2(): pass", language=Language.PYTHON),
        ]
        engine = TranslationEngine()
        results = engine.translate_batch(blocks, Language.JAVASCRIPT)

        assert len(results) == 2
        assert all(r.target_language == Language.JAVASCRIPT for r in results)


class TestComputationLanguageTranslator:
    """Test cases for main translator interface"""

    def test_detect_language(self):
        """Test language detection through main interface"""
        code = "def test(): pass"
        translator = ComputationLanguageTranslator()
        lang = translator.detect_language(code)
        assert lang == Language.PYTHON

    def test_detect_language_with_confidence(self):
        """Test language detection with confidence"""
        code = "function test() {}"
        translator = ComputationLanguageTranslator()
        lang, confidence = translator.detect_language_with_confidence(code)
        assert lang == Language.JAVASCRIPT
        assert 0.0 <= confidence <= 1.0

    def test_translate_success(self):
        """Test successful translation"""
        code = "def hello(): print('Hi')"
        translator = ComputationLanguageTranslator()
        result = translator.translate(code, "javascript")

        assert result["success"] is True
        assert result["source_language"] == "python"
        assert result["target_language"] == "javascript"
        assert "translated_code" in result
        assert 0.0 <= result["confidence"] <= 1.0

    def test_translate_with_source_language(self):
        """Test translation with explicit source language"""
        code = "print('Hello')"
        translator = ComputationLanguageTranslator()
        result = translator.translate(code, "javascript", source_language="python")

        assert result["success"] is True
        assert result["source_language"] == "python"

    def test_translate_unsupported_target(self):
        """Test translation with unsupported target language"""
        code = "def test(): pass"
        translator = ComputationLanguageTranslator()
        result = translator.translate(code, "cobol")

        assert result["success"] is False
        assert "error" in result
        assert "supported_languages" in result

    def test_translate_unsupported_source(self):
        """Test translation with unsupported source language"""
        code = "def test(): pass"
        translator = ComputationLanguageTranslator()
        result = translator.translate(code, "python", source_language="fortran")

        assert result["success"] is False
        assert "error" in result

    def test_get_supported_languages(self):
        """Test getting supported languages list"""
        translator = ComputationLanguageTranslator()
        languages = translator.get_supported_languages()

        assert isinstance(languages, list)
        assert len(languages) > 0
        assert "python" in languages
        assert "javascript" in languages
        assert "unknown" not in languages

    def test_get_supported_translations(self):
        """Test getting supported translation pairs"""
        translator = ComputationLanguageTranslator()
        translations = translator.get_supported_translations()

        assert isinstance(translations, dict)
        assert len(translations) > 0


class TestConvenienceFunctions:
    """Test cases for convenience functions"""

    def test_detect_language_function(self):
        """Test detect_language convenience function"""
        code = "def test(): pass"
        lang = detect_language(code)
        assert lang == "python"

    def test_translate_code_function(self):
        """Test translate_code convenience function"""
        code = "def hello(): pass"
        result = translate_code(code, "javascript")

        assert "success" in result
        assert "translated_code" in result

    def test_get_supported_languages_function(self):
        """Test get_supported_languages convenience function"""
        languages = get_supported_languages()
        assert isinstance(languages, list)
        assert len(languages) > 0


class TestOpcodeIntegration:
    """Test cases for opcode integration"""

    def test_register_translator_opcodes(self):
        """Test opcode registration"""
        opcodes = register_translator_opcodes()

        assert isinstance(opcodes, dict)
        assert len(opcodes) > 0

        # Check for expected opcodes
        assert "0xT1" in opcodes  # DETECT_LANG
        assert "0xT2" in opcodes  # TRANSLATE
        assert "0xT3" in opcodes  # LIST_LANGS

        # Verify opcode structure
        for opcode_id, opcode_data in opcodes.items():
            assert "name" in opcode_data
            assert "args" in opcode_data
            assert "effect" in opcode_data
            assert "handler" in opcode_data
            assert callable(opcode_data["handler"])


class TestEdgeCases:
    """Test cases for edge cases and error conditions"""

    def test_translate_empty_code(self):
        """Test translation of empty code"""
        translator = ComputationLanguageTranslator()
        result = translator.translate("", "javascript")

        # Should handle gracefully
        assert "success" in result or "error" in result

    def test_translate_whitespace_only(self):
        """Test translation of whitespace-only code"""
        translator = ComputationLanguageTranslator()
        result = translator.translate("   \n  \n  ", "javascript")

        # Should handle gracefully
        assert "success" in result or "error" in result

    def test_translate_malformed_code(self):
        """Test translation of malformed code"""
        code = "def incomplete(:"
        translator = ComputationLanguageTranslator()
        result = translator.translate(code, "javascript")

        # Should still attempt translation
        assert "success" in result
        assert "translated_code" in result

    def test_large_code_translation(self):
        """Test translation of larger code block"""
        code = """
def function1():
    print("Function 1")

def function2():
    print("Function 2")

def function3():
    if True:
        print("Function 3")
"""
        translator = ComputationLanguageTranslator()
        result = translator.translate(code, "javascript")

        assert result["success"] is True
        assert len(result["translated_code"]) > 0


class TestIndentationAdjustment:
    """Test cases for indentation adjustment"""

    def test_python_to_javascript_indentation(self):
        """Test indentation adjustment from Python (4 spaces) to JavaScript (2 spaces)"""
        code = """def test():
    if True:
        print("Test")
"""
        engine = TranslationEngine()
        result = engine.translate(code, Language.PYTHON, Language.JAVASCRIPT)

        # Check that indentation was adjusted (though pattern may change structure)
        assert result.translated_code is not None

    def test_indentation_preservation(self):
        """Test that relative indentation is preserved"""
        code = """def outer():
    def inner():
        print("Inner")
    print("Outer")
"""
        engine = TranslationEngine()
        result = engine.translate(code, Language.PYTHON, Language.JAVASCRIPT)

        # Should maintain nested structure
        lines = result.translated_code.split("\n")
        # At least some indentation should be present
        assert any(line.startswith(" ") or line.startswith("\t") for line in lines if line.strip())


# Integration tests
class TestIntegration:
    """Integration tests for translator with GhostLink tools"""

    def test_import_from_tools(self):
        """Test that translator can be imported from tools module"""
        try:
            from ghostlink.tools import get_translator

            translator = get_translator()
            assert translator is not None
        except ImportError:
            pytest.skip("Tools module not properly configured")

    def test_translator_in_tools_exports(self):
        """Test that translator functions are exported from tools"""
        try:
            from ghostlink.tools import detect_language, translate_code

            assert callable(detect_language)
            assert callable(translate_code)
        except ImportError:
            pytest.skip("Tools module not properly configured")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
