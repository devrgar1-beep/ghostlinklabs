import axios from 'axios';
import { Code, Globe, Monitor, Play, RefreshCw, Square } from 'lucide-react';
import React, { useState } from 'react';
import './ChromiumBrowser.css';

interface BrowserState {
    isRunning: boolean;
    currentUrl: string;
    pageTitle: string;
    screenshot: string | null;
    consoleLogs: string[];
    networkRequests: any[];
}

interface AutomationScript {
    name: string;
    description: string;
    script: string;
}

const ChromiumBrowser: React.FC = () => {
    const [browserState, setBrowserState] = useState<BrowserState>({
        isRunning: false,
        currentUrl: 'https://www.google.com',
        pageTitle: '',
        screenshot: null,
        consoleLogs: [],
        networkRequests: []
    });

    const [urlInput, setUrlInput] = useState(browserState.currentUrl);
    const [isLoading, setIsLoading] = useState(false);
    const [automationScripts] = useState<AutomationScript[]>([
        {
            name: 'Form Filler',
            description: 'Automatically fill out web forms',
            script: `
        // Example: Fill out a contact form
        await page.type('input[name="name"]', 'GhostLink User');
        await page.type('input[name="email"]', 'user@ghostlink.ai');
        await page.type('textarea[name="message"]', 'Hello from GhostLink automation!');
        await page.click('button[type="submit"]');
      `
        },
        {
            name: 'Data Scraper',
            description: 'Extract data from web pages',
            script: `
        // Example: Scrape product information
        const products = await page.$$eval('.product', elements =>
          elements.map(el => ({
            title: el.querySelector('.title')?.textContent,
            price: el.querySelector('.price')?.textContent,
            link: el.querySelector('a')?.href
          }))
        );
        console.log('Scraped products:', products);
      `
        },
        {
            name: 'Screenshot Taker',
            description: 'Take screenshots of web pages',
            script: `
        // Take a full page screenshot
        await page.screenshot({ path: 'screenshot.png', fullPage: true });
        console.log('Screenshot saved');
      `
        }
    ]);

    const [selectedScript, setSelectedScript] = useState<string>('');
    const [customScript, setCustomScript] = useState<string>('');

    // API endpoints for Chromium integration
    const API_BASE = 'http://localhost:8081/api/chromium';

    const startBrowser = async () => {
        setIsLoading(true);
        try {
            await axios.post(`${API_BASE}/start`);
            setBrowserState((prev: BrowserState) => ({
                ...prev,
                isRunning: true,
                consoleLogs: [...prev.consoleLogs, 'Browser started successfully']
            }));
        } catch (error: any) {
            console.error('Failed to start browser:', error);
            setBrowserState((prev: BrowserState) => ({
                ...prev,
                consoleLogs: [...prev.consoleLogs, `Error: Failed to start browser - ${error.message}`]
            }));
        }
        setIsLoading(false);
    };

    const stopBrowser = async () => {
        setIsLoading(true);
        try {
            await axios.post(`${API_BASE}/stop`);
            setBrowserState((prev: BrowserState) => ({
                ...prev,
                isRunning: false,
                consoleLogs: [...prev.consoleLogs, 'Browser stopped']
            }));
        } catch (error: any) {
            console.error('Failed to stop browser:', error);
        }
        setIsLoading(false);
    };

    const navigateToUrl = async () => {
        if (!browserState.isRunning) return;

        setIsLoading(true);
        try {
            const response = await axios.post(`${API_BASE}/navigate`, { url: urlInput });
            const data = response.data;

            setBrowserState((prev: BrowserState) => ({
                ...prev,
                currentUrl: urlInput,
                pageTitle: data.title || '',
                screenshot: data.screenshot || null,
                consoleLogs: [...prev.consoleLogs, `Navigated to: ${urlInput}`]
            }));
        } catch (error: any) {
            console.error('Failed to navigate:', error);
            setBrowserState((prev: BrowserState) => ({
                ...prev,
                consoleLogs: [...prev.consoleLogs, `Error: Failed to navigate - ${error.message}`]
            }));
        }
        setIsLoading(false);
    };

    const takeScreenshot = async () => {
        if (!browserState.isRunning) return;

        setIsLoading(true);
        try {
            const response = await axios.post(`${API_BASE}/screenshot`);
            const data = response.data;

            setBrowserState((prev: BrowserState) => ({
                ...prev,
                screenshot: data.screenshot,
                consoleLogs: [...prev.consoleLogs, 'Screenshot taken']
            }));
        } catch (error: any) {
            console.error('Failed to take screenshot:', error);
        }
        setIsLoading(false);
    };

    const runAutomationScript = async (script: string) => {
        if (!browserState.isRunning) return;

        setIsLoading(true);
        try {
            const response = await axios.post(`${API_BASE}/execute`, { script });
            const data = response.data;

            setBrowserState((prev: BrowserState) => ({
                ...prev,
                consoleLogs: [...prev.consoleLogs, `Script executed: ${data.result || 'Success'}`]
            }));
        } catch (error: any) {
            console.error('Failed to execute script:', error);
            setBrowserState((prev: BrowserState) => ({
                ...prev,
                consoleLogs: [...prev.consoleLogs, `Error: Script execution failed - ${error.message}`]
            }));
        }
        setIsLoading(false);
    };

    const handleScriptSelect = (scriptName: string) => {
        const script = automationScripts.find((s: AutomationScript) => s.name === scriptName);
        if (script) {
            setSelectedScript(scriptName);
            setCustomScript(script.script);
        }
    };

    return (
        <div className="chromium-browser">
            <div className="browser-controls">
                <div className="control-group">
                    <button
                        onClick={browserState.isRunning ? stopBrowser : startBrowser}
                        disabled={isLoading}
                        className={`control-btn ${browserState.isRunning ? 'stop' : 'start'}`}
                    >
                        {browserState.isRunning ? <Square size={16} /> : <Play size={16} />}
                        {browserState.isRunning ? 'Stop Browser' : 'Start Browser'}
                    </button>

                    <button
                        onClick={takeScreenshot}
                        disabled={!browserState.isRunning || isLoading}
                        className="control-btn screenshot"
                    >
                        <Monitor size={16} />
                        Screenshot
                    </button>
                </div>

                <div className="url-bar">
                    <Globe size={16} />
                    <input
                        type="url"
                        value={urlInput}
                        onChange={(e) => setUrlInput(e.target.value)}
                        placeholder="Enter URL..."
                        disabled={!browserState.isRunning}
                    />
                    <button
                        onClick={navigateToUrl}
                        disabled={!browserState.isRunning || isLoading}
                        className="navigate-btn"
                    >
                        <RefreshCw size={16} />
                    </button>
                </div>
            </div>

            <div className="browser-content">
                <div className="automation-panel">
                    <h3><Code size={16} /> Automation Scripts</h3>

                    <div className="script-selector">
                        <select
                            value={selectedScript}
                            onChange={(e) => handleScriptSelect(e.target.value)}
                        >
                            <option value="">Select a script...</option>
                            {automationScripts.map(script => (
                                <option key={script.name} value={script.name}>
                                    {script.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <textarea
                        value={customScript}
                        onChange={(e) => setCustomScript(e.target.value)}
                        placeholder="Enter custom JavaScript code to execute..."
                        rows={8}
                        disabled={!browserState.isRunning}
                    />

                    <button
                        onClick={() => runAutomationScript(customScript)}
                        disabled={!browserState.isRunning || isLoading || !customScript.trim()}
                        className="execute-btn"
                    >
                        <Play size={16} />
                        Execute Script
                    </button>
                </div>

                <div className="browser-view">
                    {browserState.screenshot ? (
                        <img
                            src={`data:image/png;base64,${browserState.screenshot}`}
                            alt="Browser screenshot"
                            className="screenshot-display"
                        />
                    ) : (
                        <div className="placeholder">
                            <Monitor size={48} />
                            <p>Browser not started or no screenshot available</p>
                            {browserState.pageTitle && <p>Current page: {browserState.pageTitle}</p>}
                        </div>
                    )}
                </div>

                <div className="console-panel">
                    <h3>Console Output</h3>
                    <div className="console-logs">
                        {browserState.consoleLogs.map((log, index) => (
                            <div key={index} className="log-entry">
                                <span className="timestamp">
                                    {new Date().toLocaleTimeString()}
                                </span>
                                <span className="message">{log}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChromiumBrowser;