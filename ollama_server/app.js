let OLLAMA_HOST = localStorage.getItem('ollama_host') || 'http://localhost:11434';
let MODEL_NAME = localStorage.getItem('ollama_model') || 'techcorp-finance';

const messagesContainer = document.getElementById('messages-container');
const userInput = document.getElementById('user-input');
const chatForm = document.getElementById('chat-form');
const statusDot = document.getElementById('status-dot');
const statusLabel = document.getElementById('status-label');

let connectionCheckInterval;

// Load history on start
document.addEventListener('DOMContentLoaded', () => {
    loadChatHistory();
    initSettings();
    checkConnection();
    connectionCheckInterval = setInterval(checkConnection, 5000);
});

// Load Settings into Inputs
function initSettings() {
    document.getElementById('setting-endpoint').value = OLLAMA_HOST;
    document.getElementById('setting-model').value = MODEL_NAME;
    updateDisplays();
}

function updateDisplays() {
    document.getElementById('active-model-display').textContent = `Ollama AI (${MODEL_NAME})`;
    try {
        const url = new URL(OLLAMA_HOST);
        document.getElementById('active-endpoint-display').textContent = url.host;
    } catch(e) {
        document.getElementById('active-endpoint-display').textContent = OLLAMA_HOST;
    }
}

function applySettings() {
    const endpointInput = document.getElementById('setting-endpoint').value.trim();
    const modelInput = document.getElementById('setting-model').value.trim();
    
    if (!endpointInput || !modelInput) {
        alert('Veuillez remplir tous les champs.');
        return;
    }
    
    OLLAMA_HOST = endpointInput;
    MODEL_NAME = modelInput;
    
    localStorage.setItem('ollama_host', OLLAMA_HOST);
    localStorage.setItem('ollama_model', MODEL_NAME);
    
    updateDisplays();
    checkConnection();
    
    // Visual feedback for applying settings
    const btn = document.getElementById('save-settings-btn');
    btn.textContent = 'Appliqué !';
    btn.style.backgroundColor = 'var(--success)';
    setTimeout(() => {
        btn.textContent = 'Appliquer';
        btn.style.backgroundColor = 'var(--primary)';
    }, 1500);
}

// Check connection to Ollama Server
async function checkConnection() {
    try {
        const response = await fetch(`${OLLAMA_HOST}/api/tags`, {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        });
        
        if (response.ok) {
            statusDot.className = 'status-dot connected';
            statusLabel.textContent = 'Serveur Connecté';
        } else {
            throw new Error();
        }
    } catch (e) {
        statusDot.className = 'status-dot disconnected';
        statusLabel.textContent = 'Serveur Déconnecté';
    }
}

// Send user message
async function sendMessage(event) {
    event.preventDefault();
    const text = userInput.value.trim();
    if (!text) return;

    // Add User Message to UI & Save
    appendMessage(text, 'user');
    saveMessage(text, 'user');
    userInput.value = '';

    // Add Loading message
    const botMessageEl = appendMessage('En cours de traitement...', 'assistant loading');

    try {
        const response = await fetch(`${OLLAMA_HOST}/api/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: MODEL_NAME,
                prompt: text,
                stream: false
            })
        });

        if (!response.ok) throw new Error('Erreur de communication avec le serveur Ollama.');

        const data = await response.json();
        
        // Remove loading state and set response
        botMessageEl.classList.remove('loading');
        botMessageEl.querySelector('.message-content').textContent = data.response;
        saveMessage(data.response, 'assistant');

    } catch (error) {
        botMessageEl.classList.remove('loading');
        botMessageEl.querySelector('.message-content').textContent = `Erreur: Impossible de contacter le serveur d'inférence.`;
        botMessageEl.querySelector('.message-content').style.color = 'var(--danger)';
    }

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Append message block helper
function appendMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return messageDiv;
}

// History Management
function saveMessage(text, sender) {
    const history = JSON.parse(localStorage.getItem('techcorp_chat_history') || '[]');
    history.push({ text, sender });
    localStorage.setItem('techcorp_chat_history', JSON.stringify(history));
}

function loadChatHistory() {
    const history = JSON.parse(localStorage.getItem('techcorp_chat_history') || '[]');
    if (history.length > 0) {
        messagesContainer.innerHTML = '';
        history.forEach(msg => {
            appendMessage(msg.text, msg.sender);
        });
    }
}

// Clear chat logs
function clearChat() {
    localStorage.removeItem('techcorp_chat_history');
    messagesContainer.innerHTML = `
        <div class="message system-message">
            <div class="message-content">
                <h3>Nouvelle Session Démarrée</h3>
                <p>Posez vos questions financières de manière sécurisée.</p>
            </div>
        </div>
    `;
}
