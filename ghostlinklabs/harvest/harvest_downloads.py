from datetime import datetime
import json
from pathlib import Path
import shutil

SOURCE_DIR = Path("/Users/ghostlink/Downloads")
DEST_DIR = Path(
    "/Users/ghostlink/Library/Mobile Documents/com~apple~CloudDocs/ghostlinklabs/harvest/downloads"
)
MANIFEST_FILE = DEST_DIR.parent / "harvest_manifest.json"

EXCLUDE_EXTENSIONS = {".iso", ".dmg", ".zip", ".tar.gz", ".tgz"}
# We exclude large archives and installers, but keep code/text.


def harvest():
    if not DEST_DIR.exists():
        DEST_DIR.mkdir(parents=True)

    manifest = {
        "timestamp": datetime.now().isoformat(),
        "source": str(SOURCE_DIR),
        "destination": str(DEST_DIR),
        "copied_files": [],
        "skipped_files": [],
        "errors": [],
    }

    print(f"Harvesting from {SOURCE_DIR} to {DEST_DIR}...")

    for item in SOURCE_DIR.iterdir():
        try:
            if item.name.startswith("."):
                continue

            if item.is_file():
                if item.suffix.lower() in EXCLUDE_EXTENSIONS:
                    print(f"Skipping large file: {item.name}")
                    manifest["skipped_files"].append(item.name)
                    continue

                dest_path = DEST_DIR / item.name
                shutil.copy2(item, dest_path)
                manifest["copied_files"].append(item.name)
                print(f"Copied: {item.name}")

            elif item.is_dir():
                # For directories, we copy recursively but skip if it looks like a large app or cache
                if item.name.endswith(".app") or item.name.endswith(".download"):
                    print(f"Skipping directory: {item.name}")
                    manifest["skipped_files"].append(item.name)
                    continue

                dest_path = DEST_DIR / item.name
                if dest_path.exists():
                    shutil.rmtree(dest_path)
                shutil.copytree(item, dest_path, dirs_exist_ok=True)
                manifest["copied_files"].append(f"{item.name}/")
                print(f"Copied directory: {item.name}")

        except Exception as e:
            print(f"Error copying {item.name}: {e}")
            manifest["errors"].append({"file": item.name, "error": str(e)})

    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Harvest complete. Manifest saved to {MANIFEST_FILE}")


if __name__ == "__main__":
    harvest()
