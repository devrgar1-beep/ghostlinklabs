#!/usr/bin/env python3
"""Generate a static HTML viewer that loads the mental model and provenance summary.

Outputs: /Users/ghostlink/ghostlink-wiki-organized/viewer/index.html
"""
from pathlib import Path

WORK_DIR = Path('/Users/ghostlink/ghostlink-wiki-organized')
OUT_DIR = WORK_DIR / 'viewer'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Copy JSON artifacts into viewer dir (if they exist)
ARTIFACTS = [
    'ghostlink_mental_model.json',
    'ghostlink_provenance_summary.json',
    'ghostlink_provenance_index.json',
    'ghostlink_refactor_dryrun.json'
]

for a in ARTIFACTS:
    src = WORK_DIR / a
    dst = OUT_DIR / a
    if src.exists():
        with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
            fdst.write(fsrc.read())

html = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>GhostLink Mental Model Viewer</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; max-width: 1100px; }
    h1 { color: #0c4a6e; }
    pre { background: #f6f8fa; padding: 10px; border-radius: 6px; overflow-x:auto; }
    .columns { display:flex; gap:20px; }
    .col { flex:1; min-width: 300px; }
    .file-list { height: 500px; overflow: auto; border: 1px solid #ddd; padding: 8px; background: #fff; }
    input[type=search] { width: 100%; padding: 8px; margin-bottom: 10px; }
  </style>
</head>
<body>
  <h1>GhostLink Mental Model & Provenance Viewer</h1>
  <p>Provides a quick view of the mental model, provenance summary, and refactor dry-run results. Files are snapshots created by the automation pipeline.</p>

  <div class="columns">
    <div class="col">
      <h2>Mental Model</h2>
      <pre id="mental"></pre>
    </div>
    <div class="col">
      <h2>Provenance Summary</h2>
      <input type="search" id="search" placeholder="Search by filename or term"/>
      <div class="file-list" id="fileList"></div>
    </div>
  </div>

  <h2>Refactor Dry-Run</h2>
  <pre id="dryrun"></pre>

  <script>
    async function loadJSON(path) {
      try {
        const resp = await fetch(path);
        if(!resp.ok) return null;
        return await resp.json();
      } catch(e) { console.error(e); return null; }
    }

    async function init() {
      const mental = await loadJSON('ghostlink_mental_model.json');
      const summary = await loadJSON('ghostlink_provenance_summary.json');
      const dryrun = await loadJSON('ghostlink_refactor_dryrun.json');

      if(mental) document.getElementById('mental').textContent = JSON.stringify(mental, null, 2);
      if(dryrun) document.getElementById('dryrun').textContent = JSON.stringify(dryrun, null, 2);

      const fileListEl = document.getElementById('fileList');
      if(summary && summary.files) {
        summary.files.slice(0,500).forEach(f => {
          const el = document.createElement('div');
          el.innerHTML = `<strong>${f.file}</strong> - matches: ${f.match_count}<br/><em>top: ${f.top_terms.join(', ')}</em>`;
          fileListEl.appendChild(el);
        });
      }

      document.getElementById('search').addEventListener('input', (e) => {
        const q = e.target.value.toLowerCase().trim();
        fileListEl.innerHTML = '';
        const files = (summary && summary.files) ? summary.files : [];
        files.filter(f => f.file.toLowerCase().includes(q) || f.top_terms.join(' ').toLowerCase().includes(q)).slice(0,500).forEach(f => {
          const el = document.createElement('div');
          el.innerHTML = `<strong>${f.file}</strong> - matches: ${f.match_count}<br/><em>top: ${f.top_terms.join(', ')}</em>`;
          fileListEl.appendChild(el);
        });
      });
    }

    init();
  </script>
</body>
</html>
"""

OUT_HTML = OUT_DIR / 'index.html'
with open(OUT_HTML, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Writer viewer to {OUT_HTML}')
