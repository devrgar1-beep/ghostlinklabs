GhostLink Explorer

This is a simple static viewer for quick inspection of generated artifacts.

Files it expects (relative to `viewer/index.html`):
- `../ghostlink_mental_model.json`
- `../ghostlink_provenance_summary.json`
- `../ghostlink_legacy_mapping.json`

Usage:
- Open `viewer/index.html` in a browser (file:// works for modern browsers).
- Use the refresh buttons to reload JSON files after running the automation pipeline.

If files are large, consider copying a subset into the viewer folder or run a local static server:

```bash
# From /Users/ghostlink/ghostlink-wiki-organized/
python3 -m http.server 8000
# then open http://localhost:8000/viewer/
```
