#!/usr/bin/env python3
"""
Quick Reference Index Generator for GhostLink Project
Creates a searchable index of all files with categories and descriptions.
"""

import json
from pathlib import Path
from typing import Any, Dict


def categorize_file(file_path: Path) -> str:
    """Categorize a file based on its path and extension."""
    name = file_path.name.lower()
    ext = file_path.suffix.lower()
    parent = file_path.parent.name.lower()

    # Core modules
    if "ghostlink/core" in str(file_path):
        return "core"

    # Interfaces
    if "ghostlink/interfaces" in str(file_path):
        return "interfaces"

    # Utils
    if "ghostlink/utils" in str(file_path):
        return "utils"

    # Documentation
    if ext in [".md", ".txt", ".pdf", ".docx"] and "readme" in name:
        return "documentation"
    if "doc" in parent or "docs" in parent:
        return "documentation"

    # Scripts
    if ext == ".py" and ("script" in name or "demo" in name or "test" in name):
        return "scripts"
    if "scripts" in parent:
        return "scripts"

    # Configuration
    if ext in [".yaml", ".yml", ".json", ".env", ".cfg"]:
        return "configuration"
    if "config" in name:
        return "configuration"

    # Archives
    if ext in [".zip", ".tgz", ".tar.gz"]:
        return "archives"

    # Logs
    if "log" in name or "logs" in parent:
        return "logs"

    # Notes
    if ext == ".txt" and any(char.isdigit() for char in name):
        return "notes"

    # Images
    if ext in [".png", ".jpg", ".jpeg", ".gif"]:
        return "images"

    # Other
    return "other"


def generate_index(root_path: str) -> Dict[str, Any]:
    """Generate a categorized index of all files."""
    root = Path(root_path)
    index: Dict[str, Any] = {"categories": {}, "files": {}, "stats": {}}

    categories: Dict[str, list] = {}

    for file_path in root.rglob("*"):
        if file_path.is_file():
            category = categorize_file(file_path)
            relative_path = file_path.relative_to(root)

            if category not in categories:
                categories[category] = []

            file_info = {
                "path": str(relative_path),
                "name": file_path.name,
                "size": file_path.stat().st_size,
                "modified": file_path.stat().st_mtime,
            }

            categories[category].append(file_info)
            index["files"][str(relative_path)] = {"category": category, "info": file_info}

    index["categories"] = categories
    index["stats"] = {
        "total_files": len(index["files"]),
        "categories_count": len(categories),
        "total_size": sum(f["info"]["size"] for f in index["files"].values()),
    }

    return index


def main():
    """Main function to generate and save the index."""
    project_root = Path(__file__).parent
    index = generate_index(str(project_root))

    # Save to JSON
    index_file = project_root / "project_index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"Index generated with {index['stats']['total_files']} files")
    print(f"Saved to: {index_file}")

    # Print summary
    print("\nCategory Summary:")
    for cat, files in index["categories"].items():
        print(f"  {cat}: {len(files)} files")


if __name__ == "__main__":
    main()
