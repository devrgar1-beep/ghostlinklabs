const API_URL = 'http://localhost:8000';

async function fetchStatus() {
  const res = await fetch(`${API_URL}/status`);
  if (!res.ok) throw new Error('Failed to fetch status');
  return res.json();
}

async function triggerEvolve() {
  const res = await fetch(`${API_URL}/evolve`, {method: 'POST'});
  return res.json();
}

function renderStatus(status) {
  const container = document.getElementById('status');
  container.innerHTML = `\n    <div><span class="key">Current Generation:</span> ${status.current_generation}</div>\n    <div><span class="key">Fitness:</span> ${status.current_fitness.toFixed(3)}</div>\n    <div><span class="key">Genetic Pool:</span> ${status.genetic_pool_size}</div>\n    <div><span class="key">Learning Cycles:</span> ${status.learning_cycles}</div>\n    <div><span class="key">Quantum:</span> ${status.quantum_capabilities.available}</div>\n  `;

  document.getElementById('raw').innerText = JSON.stringify(status, null, 2);
}

async function init() {
  document.getElementById('refresh').addEventListener('click', async () => {
    document.getElementById('status').innerText = 'Refreshing…';
    try {
      const status = await fetchStatus();
      renderStatus(status);
    } catch (e) {
      document.getElementById('status').innerText = 'Error fetching status: ' + e;
    }
  });

  document.getElementById('evolve').addEventListener('click', async () => {
    document.getElementById('status').innerText = 'Triggering evolution…';
    try {
      const result = await triggerEvolve();
      renderStatus(result.status);
    } catch (e) {
      document.getElementById('status').innerText = 'Error triggering evolve: ' + e;
    }
  });

  // Auto refresh once
  try {
    const status = await fetchStatus();
    renderStatus(status);
  } catch (e) {
    document.getElementById('status').innerText = 'Error fetching status: ' + e;
  }
}

init();
