#!/usr/bin/env python3
"""
GhostLink System Metadata Test
Validates system metadata structure and content
"""

import json
from pathlib import Path
import sys


def test_system_metadata():
    """Test system metadata structure and content"""

    metadata_file = Path("schemas/system_metadata.json")

    if not metadata_file.exists():
        print("❌ System metadata file not found")
        return False

    try:
        with open(metadata_file, encoding="utf-8") as f:
            metadata = json.load(f)

        print("✅ System metadata loaded successfully")

        # Test core structure
        required_sections = [
            "site_metadata",
            "core_system",
            "governance_laws",
            "technical_components",
            "canonical_taxonomy",
            "mathematical_frameworks",
            "emergent_properties",
            "system_metrics",
            "meta_descriptions",
        ]

        for section in required_sections:
            if section not in metadata:
                print(f"❌ Missing required section: {section}")
                return False
            print(f"✅ Section present: {section}")

        # Test governance laws
        laws = metadata["governance_laws"]
        expected_laws = [f"L-{i:02d}" for i in range(1, 11)]

        for law_id in expected_laws:
            if law_id not in laws:
                print(f"❌ Missing governance law: {law_id}")
                return False

        print(f"✅ All {len(expected_laws)} governance laws present")

        # Test technical components
        components = metadata["technical_components"]
        expected_components = [
            "GHOSTCORE",
            "GhostSlang",
            "Lumara_Framework",
            "DAK",
            "Component_Blueprint",
        ]

        for component in expected_components:
            if component not in components:
                print(f"❌ Missing technical component: {component}")
                return False

        print(f"✅ All {len(expected_components)} technical components present")

        # Test system metrics
        metrics = metadata["system_metrics"]
        if metrics["perfection_score"] != "99.97%":
            print("❌ Incorrect perfection score")
            return False

        print("✅ System metrics validated")

        # Test convergence rate
        core = metadata["core_system"]
        if core["convergence_rate"] != "99.97%":
            print("❌ Incorrect convergence rate")
            return False

        print("✅ Convergence rate validated")

        # Test architecture numbers
        arch = core["architecture"]
        expected = {"agents": 67, "pipelines": 14, "shards": 26, "mirror_domains": 14}

        for key, expected_value in expected.items():
            if arch[key] != expected_value:
                print(f"❌ Incorrect {key} count: {arch[key]} != {expected_value}")
                return False

        print("✅ Architecture specifications validated")

        print("\n🎉 System metadata validation complete - all tests passed!")
        return True

    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False


if __name__ == "__main__":
    success = test_system_metadata()
    sys.exit(0 if success else 1)
