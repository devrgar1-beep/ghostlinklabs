async function loadJSON(path) {
  try {
    const res = await fetch(path);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (e) {
    return { error: e.message };
  }
}

function renderJSONPre(el, data) {
  el.textContent = JSON.stringify(data, null, 2);
}

async function refreshModel() {
  const model = await loadJSON('../ghostlink_mental_model.json');
  renderJSONPre(document.getElementById('modelContent'), model);
}

async function refreshProv(filter='') {
  const prov = await loadJSON('../ghostlink_provenance_summary.json');
  const container = document.getElementById('provList');
  if (prov.error) { container.textContent = 'Error loading provenance: '+prov.error; return; }
  const keys = Object.keys(prov).filter(k => !filter || k.includes(filter) || JSON.stringify(prov[k]).includes(filter));
  container.innerHTML = '';
  if (keys.length===0) { container.textContent = 'No matches'; return; }
  for (const k of keys.sort()) {
    const div = document.createElement('div');
    div.className = 'file-item';
    div.innerHTML = `<strong>${k}</strong> — <span class="match">${prov[k].matches||0}</span> matches<br/><small>${(prov[k].summary||'').slice(0,200)}</small>`;
    container.appendChild(div);
  }
}

async function refreshMap(filter='') {
  const map = await loadJSON('../ghostlink_legacy_mapping.json');
  const container = document.getElementById('mapList');
  if (map.error) { container.textContent = 'Error loading mapping: '+map.error; return; }
  const files = Object.keys(map).filter(f => !filter || f.includes(filter) || JSON.stringify(map[f]).includes(filter));
  container.innerHTML = '';
  if (files.length===0) { container.textContent='No mapping entries found'; return; }
  for (const f of files.sort()) {
    const div = document.createElement('div');
    div.className = 'file-item';
    const hits = map[f].hits||[];
    div.innerHTML = `<strong>${f}</strong> — ${hits.length} hits`;
    const ul = document.createElement('ul');
    for (const h of hits.slice(0,10)) {
      const li = document.createElement('li');
      li.textContent = `${h.line}: ${h.original.trim().slice(0,120)}`;
      ul.appendChild(li);
    }
    div.appendChild(ul);
    container.appendChild(div);
  }
}

document.getElementById('refreshModel').addEventListener('click', () => refreshModel());
document.getElementById('refreshProv').addEventListener('click', () => refreshProv(document.getElementById('provSearch').value));
document.getElementById('refreshMap').addEventListener('click', () => refreshMap(document.getElementById('mapSearch').value));

// initial load
refreshModel();
refreshProv();
refreshMap();
