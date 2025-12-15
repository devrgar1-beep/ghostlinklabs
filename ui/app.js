/**
 * GhostLink Local - Frontend App Logic
 */

const { ipcRenderer } = require('electron');

let currentMode = 'chat';
let isProcessing = false;

// =============================================================================
// UI HELPERS
// =============================================================================

function addMessage(content, type = 'assistant') {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = content;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function getAIMode() {
    const selected = document.querySelector('input[name="aiMode"]:checked');
    return selected ? selected.value : 'fast';
}

function setProcessing(processing) {
    isProcessing = processing;
    const sendButton = document.getElementById('sendButton');
    const messageInput = document.getElementById('messageInput');
    
    sendButton.disabled = processing;
    sendButton.textContent = processing ? 'Processing...' : 'Send';
    messageInput.disabled = processing;
}

// =============================================================================
// CHAT FUNCTIONALITY
// =============================================================================

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message || isProcessing) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    input.value = '';
    
    setProcessing(true);
    
    try {
        const mode = getAIMode();
        const response = await ipcRenderer.invoke('chat', message, mode);
        
        if (response.error) {
            addMessage(`Error: ${response.error}`, 'system');
        } else {
            addMessage(response.response, 'assistant');
            
            // If consensus mode, show additional info
            if (mode === 'consensus' && response.creative) {
                addMessage(`💡 Creative perspective: ${response.creative}`, 'system');
            }
        }
    } catch (error) {
        addMessage(`Error: ${error.message}`, 'system');
    } finally {
        setProcessing(false);
    }
}

// =============================================================================
// MODE SWITCHING
// =============================================================================

function switchMode(mode) {
    currentMode = mode;
    
    // Update button states
    const buttons = document.querySelectorAll('.sidebar button');
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Clear chat
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.innerHTML = '';
    
    // Add welcome message based on mode
    if (mode === 'chat') {
        addMessage('Chat mode active. Ask me anything!', 'system');
    } else if (mode === 'code') {
        addMessage('Code analysis mode. Paste your code to analyze.', 'system');
    } else if (mode === 'refactor') {
        addMessage('Code refactor mode. Paste code and describe what you want to improve.', 'system');
    }
}

// =============================================================================
// HEALTH CHECK
// =============================================================================

async function checkHealth() {
    try {
        const health = await ipcRenderer.invoke('health-check');
        const status = document.getElementById('status');
        
        if (health.status === 'healthy') {
            status.textContent = `✅ System Healthy - ${health.connections} connections`;
            status.style.color = '#00ff88';
        } else {
            status.textContent = `⚠️ System Issues: ${health.message}`;
            status.style.color = '#ff8800';
        }
        
        setTimeout(() => {
            status.textContent = '🔒 100% Local - No External Dependencies';
            status.style.color = '#888';
        }, 3000);
        
    } catch (error) {
        const status = document.getElementById('status');
        status.textContent = `❌ Error: ${error.message}`;
        status.style.color = '#ff0000';
    }
}

// =============================================================================
// KEYBOARD SHORTCUTS
// =============================================================================

document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    
    // Send message on Cmd/Ctrl + Enter
    messageInput.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Check health on startup
    setTimeout(checkHealth, 1000);
});

// =============================================================================
// EXPORTS
// =============================================================================

window.sendMessage = sendMessage;
window.switchMode = switchMode;
window.checkHealth = checkHealth;
