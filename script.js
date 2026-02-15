import { GoogleGenerativeAI } from "@google/generative-ai";

// DOM Elements
const messagesContainer = document.getElementById("messages-container");
const promptInput = document.getElementById("prompt-input");
const sendBtn = document.getElementById("send-btn");
const uploadBtn = document.getElementById("upload-btn");
const fileUpload = document.getElementById("file-upload");
const imagePreview = document.getElementById("image-preview");
const previewContent = document.getElementById("preview-content");
const removeImageBtn = document.getElementById("remove-image");
const settingsModal = document.getElementById("settings-modal");
const settingsBtn = document.getElementById("settings-btn");
const closeModal = document.getElementById("close-modal");
const saveSettingsBtn = document.getElementById("save-settings");
const apiKeyInput = document.getElementById("api-key");
const modelSelect = document.getElementById("model-select");
const mobileMenuBtn = document.getElementById("mobile-menu-btn");
const sidebar = document.querySelector(".sidebar");
const newChatBtn = document.getElementById("new-chat-btn");
const currentModelName = document.getElementById("current-model-name");

// State
let state = {
    apiKey: localStorage.getItem("gemini_api_key") || "",
    model: localStorage.getItem("gemini_model") || "gemini-1.5-flash",
    history: [],
    currentFile: null
};

// Initialize
function init() {
    if (!state.apiKey) {
        openModal();
    }
    apiKeyInput.value = state.apiKey;
    modelSelect.value = state.model;
    updateModelDisplay();

    // Event Listeners
    sendBtn.addEventListener("click", sendMessage);
    promptInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    uploadBtn.addEventListener("click", () => fileUpload.click());
    fileUpload.addEventListener("change", handleFileUpload);
    removeImageBtn.addEventListener("click", clearFile);

    settingsBtn.addEventListener("click", openModal);
    closeModal.addEventListener("click", () => settingsModal.classList.remove("active"));
    saveSettingsBtn.addEventListener("click", saveSettings);

    mobileMenuBtn.addEventListener("click", () => sidebar.classList.toggle("open"));
    newChatBtn.addEventListener("click", startNewChat);

    // Initial check for input to enable/disable send button
    promptInput.addEventListener("input", toggleSendButton);
}

function updateModelDisplay() {
    const modelNames = {
        "gemini-1.5-flash": "Gemini 1.5 Flash",
        "gemini-1.5-pro": "Gemini 1.5 Pro"
    };
    currentModelName.textContent = modelNames[state.model] || state.model;
}

function toggleSendButton() {
    sendBtn.disabled = !promptInput.value.trim() && !state.currentFile;
}

function openModal() {
    settingsModal.classList.add("active");
}

function saveSettings() {
    const key = apiKeyInput.value.trim();
    const model = modelSelect.value;
    
    if (key) {
        state.apiKey = key;
        localStorage.setItem("gemini_api_key", key);
    }

    state.model = model;
    localStorage.setItem("gemini_model", model);
    updateModelDisplay();

    settingsModal.classList.remove("active");
    alert("Settings saved!");
}

async function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    // limit to 20MB
    if (file.size > 20 * 1024 * 1024) {
        alert("File size exceeds 20MB limit.");
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        const base64Data = e.target.result.split(',')[1];
        state.currentFile = {
            inlineData: {
                data: base64Data,
                mimeType: file.type
            },
            name: file.name,
            type: file.type,
            src: e.target.result // Keep data URL for preview
        };
        
        // Generate Preview
        previewContent.innerHTML = '';
        if (file.type.startsWith('image/')) {
            const img = document.createElement('img');
            img.src = e.target.result;
            previewContent.appendChild(img);
        } else if (file.type.startsWith('video/')) {
            const icon = document.createElement('i');
            icon.className = 'fa-solid fa-file-video';
            icon.style.fontSize = '40px';
            previewContent.appendChild(icon);
            const span = document.createElement('span');
            span.textContent = file.name;
            span.style.marginLeft = '10px';
            previewContent.appendChild(span);
        } else if (file.type.startsWith('audio/')) {
            const icon = document.createElement('i');
            icon.className = 'fa-solid fa-file-audio';
            icon.style.fontSize = '40px';
            previewContent.appendChild(icon);
            const span = document.createElement('span');
            span.textContent = file.name;
            span.style.marginLeft = '10px';
            previewContent.appendChild(span);
        }

        imagePreview.classList.remove("hidden");
        toggleSendButton();
    };
    reader.readAsDataURL(file);
}

function clearFile() {
    state.currentFile = null;
    imagePreview.classList.add("hidden");
    fileUpload.value = "";
    previewContent.innerHTML = "";
    toggleSendButton();
}

function appendMessage(role, text, fileData = null) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement("div");
    avatar.className = `avatar ${role === "user" ? "user" : "ai"}`;
    avatar.innerHTML = role === "user" ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';

    const content = document.createElement("div");
    content.className = "message-content";

    // Basic Markdown parsing (bold, code blocks)
    let formattedText = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
        .replace(/\n/g, '<br>');

    content.innerHTML = formattedText;

    if (fileData) {
        const mediaContainer = document.createElement('div');
        mediaContainer.style.marginTop = '10px';

        if (fileData.type.startsWith('image/')) {
            const img = document.createElement("img");
            img.src = fileData.src;
            img.style.maxWidth = '100%';
            img.style.borderRadius = '8px';
            mediaContainer.appendChild(img);
        } else if (fileData.type.startsWith('video/')) {
            const video = document.createElement("video");
            video.src = fileData.src;
            video.controls = true;
            video.style.maxWidth = '100%';
            video.style.borderRadius = '8px';
            mediaContainer.appendChild(video);
        } else if (fileData.type.startsWith('audio/')) {
            const audio = document.createElement("audio");
            audio.src = fileData.src;
            audio.controls = true;
            mediaContainer.appendChild(audio);
        }
        content.appendChild(mediaContainer);
    }
    
    if (role === "user") {
        messageDiv.appendChild(content);
        messageDiv.appendChild(avatar);
    } else {
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

async function sendMessage() {
    const text = promptInput.value.trim();
    if (!text && !state.currentFile) return;

    if (!state.apiKey) {
        openModal();
        return;
    }

    // Capture state at moment of sending
    const fileToSend = state.currentFile ? { ...state.currentFile } : null;

    // Add user message
    appendMessage("user", text, fileToSend);

    // Clear input
    promptInput.value = "";
    clearFile();

    // Add loading indicator
    const loadingDiv = document.createElement("div");
    loadingDiv.className = "message ai loading";
    loadingDiv.innerHTML = `<div class="avatar ai"><i class="fa-solid fa-robot"></i></div><div class="message-content">Thinking...</div>`;
    messagesContainer.appendChild(loadingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    try {
        const genAI = new GoogleGenerativeAI(state.apiKey);
        const model = genAI.getGenerativeModel({ model: state.model });

        const prompt = text || "Describe this file.";
        const parts = [prompt];
        if (fileToSend) {
            // Only send the inlineData part to the API
            parts.push(fileToSend.inlineData);
        }

        const result = await model.generateContent(parts);
        const response = await result.response;
        const textResponse = response.text();

        // Remove loading
        messagesContainer.removeChild(loadingDiv);

        appendMessage("ai", textResponse);

    } catch (error) {
        messagesContainer.removeChild(loadingDiv);
        appendMessage("ai", `Error: ${error.message}`);
        console.error(error);
        if (error.message.includes("API key")) {
            openModal();
        }
    }
}

function startNewChat() {
    messagesContainer.innerHTML = `
        <div class="welcome-message">
            <h1>How can I help you today?</h1>
            <p>I can generate text, analyze images, and assist with code.</p>
        </div>
    `;
    state.history = [];
}

init();
