import React from 'react';
import ChromiumBrowser from './components/ChromiumBrowser';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>GhostLink Control Panel</h1>
        <p>AI-Powered Automation with Chromium Integration</p>
      </header>
      <main>
        <ChromiumBrowser />
      </main>
    </div>
  );
}

export default App;