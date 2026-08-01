document.addEventListener("DOMContentLoaded", () => {
    // ==========================================
    // 1. Cache DOM Elements
    // ==========================================
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatMessages = document.getElementById("chat-messages");
    const connectionStatus = document.getElementById("connection-status");
    const navLinks = document.querySelectorAll(".nav-link");
    const navSyncBtn = document.getElementById("nav-sync-btn");
    
    // View sections
    const viewChat = document.getElementById("view-chat");
    const viewHealth = document.getElementById("view-health");

    // ==========================================
    // 2. Check Backend Health on Page Load
    // ==========================================
    async function checkHealth() {
        try {
            const response = await fetch("/health");
            if (response.ok) {
                const data = await response.json();
                updateConnectionStatus(true, data.status || "Connected");
            } else {
                updateConnectionStatus(false, "Server Error");
            }
        } catch (error) {
            console.error("Health check failed:", error);
            updateConnectionStatus(false, "Disconnected");
        }
    }

    function updateConnectionStatus(isConnected, message = "Connected") {
        if (!connectionStatus) return;
        if (isConnected) {
            connectionStatus.className = "badge bg-success";
            connectionStatus.innerHTML = `<i class="bi bi-circle-fill me-1 small"></i>${message}`;
        } else {
            connectionStatus.className = "badge bg-danger";
            connectionStatus.innerHTML = `<i class="bi bi-circle-fill me-1 small"></i>${message}`;
        }
    }

    checkHealth();

    // ==========================================
    // 3. Register Sidebar Actions & View Switching
    // ==========================================
    navLinks.forEach(link => {
        link.addEventListener("click", async (e) => {
            e.preventDefault();
            
            navLinks.forEach(l => l.classList.remove("active"));
            navLinks.forEach(l => l.classList.add("text-dark"));
            
            link.classList.add("active");
            link.classList.remove("text-dark");

            const section = link.getAttribute("data-section");

            // Handle View Display toggles
            if (section === "health") {
                if (viewChat) viewChat.classList.add("d-none");
                if (viewHealth) viewHealth.classList.remove("d-none");
                await checkHealth();
            } else {
                if (viewHealth) viewHealth.classList.add("d-none");
                if (viewChat) viewChat.classList.remove("d-none");

                if (section === "synchronize") {
                    await triggerSynchronization();
                }
            }
        });
    });

    // Top-bar sync button handler
    if (navSyncBtn) {
        navSyncBtn.addEventListener("click", async () => {
            // Switch back to chat view if user was elsewhere
            if (viewHealth) viewHealth.classList.add("d-none");
            if (viewChat) viewChat.classList.remove("d-none");
            await triggerSynchronization();
        });
    }

    async function triggerSynchronization() {
        appendSystemMessage("Triggering SharePoint synchronization...");
        try {
            const response = await fetch("/sync", { method: "POST" });
            const data = await response.json();
            if (response.ok) {
                appendSystemMessage(data.message || "Synchronization completed successfully.");
            } else {
                appendSystemMessage(`Synchronization failed: ${data.detail || "Unknown error"}`);
            }
        } catch (error) {
            console.error("Sync error:", error);
            appendSystemMessage("Error connecting to server for synchronization.");
        }
    }

    // ==========================================
    // 4. Attach Form Submit Handler & Chat Logic
    // ==========================================
    if (chatForm) {
        chatForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const query = userInput.value.trim();
            if (!query) return;

            appendUserMessage(query);
            userInput.value = "";
            scrollToBottom();

            const loadingId = appendLoadingIndicator();
            scrollToBottom();

            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    body: JSON.stringify({ question: query })
                });

                removeLoadingIndicator(loadingId);

                if (!response.ok) {
                    throw new Error(`Server returned status ${response.status}`);
                }

                const data = await response.json();
                
                const reply = data.answer || data.response || "No response received.";
                const sources = data.sources || data.citations || [];
                const confidence = data.confidence !== undefined ? data.confidence : null;

                appendAssistantMessage(reply, sources, confidence);

            } catch (error) {
                console.error("Chat API error:", error);
                removeLoadingIndicator(loadingId);
                appendAssistantMessage("Sorry, I encountered an error communicating with the server. Please try again.", [], null);
            }

            scrollToBottom();
        });
    }

    // ==========================================
    // 5. DOM Rendering Helper Functions
    // ==========================================
    function appendUserMessage(text) {
        const timeString = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const html = `
            <div class="d-flex mb-3 justify-content-end">
                <div class="me-3 text-end flex-grow-1">
                    <div class="card bg-primary text-white border-0 p-3 shadow-sm d-inline-block text-start">
                        <p class="mb-0">${escapeHTML(text)}</p>
                    </div>
                    <small class="text-muted mt-1 me-1 d-block">${timeString}</small>
                </div>
                <div class="flex-shrink-0 bg-dark text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                    <i class="bi bi-person"></i>
                </div>
            </div>
        `;
        chatMessages.insertAdjacentHTML("beforeend", html);
    }

    function appendAssistantMessage(text, sources = [], confidence = null) {
        const timeString = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        let sourcesHtml = '';
        if (sources && sources.length > 0) {
            const badges = sources.map(source => `<span class="badge bg-secondary text-white me-1 mb-1">${escapeHTML(typeof source === 'string' ? source : source.title || source.name || 'Document')}</span>`).join('');
            sourcesHtml = `
                <div class="sources-container mt-2 pt-2 border-top d-flex flex-wrap align-items-center gap-1">
                    <span class="small text-muted fw-bold me-1"><i class="bi bi-journal-text"></i> Sources:</span>
                    ${badges}
                </div>
            `;
        }

        let confidenceHtml = '';
        if (confidence !== null) {
            const formattedConfidence = typeof confidence === 'number' && confidence <= 1 ? Math.round(confidence * 100) + '%' : confidence;
            confidenceHtml = `
                <div class="confidence-container mt-2">
                    <span class="badge bg-info text-dark">Confidence: ${escapeHTML(String(formattedConfidence))}</span>
                </div>
            `;
        }

        const html = `
            <div class="d-flex mb-3">
                <div class="flex-shrink-0 bg-secondary text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                    <i class="bi bi-robot"></i>
                </div>
                <div class="ms-3 flex-grow-1">
                    <div class="card bg-light border-0 p-3 shadow-sm">
                        <p class="mb-2">${escapeHTML(text)}</p>
                        ${sourcesHtml}
                        ${confidenceHtml}
                    </div>
                    <small class="text-muted mt-1 ms-1 d-block">${timeString}</small>
                </div>
            </div>
        `;
        chatMessages.insertAdjacentHTML("beforeend", html);
    }

    function appendSystemMessage(text) {
        const html = `
            <div class="text-center my-3">
                <span class="badge bg-secondary text-light px-3 py-2">${escapeHTML(text)}</span>
            </div>
        `;
        chatMessages.insertAdjacentHTML("beforeend", html);
        scrollToBottom();
    }

    function appendLoadingIndicator() {
        const id = 'loading-' + Date.now();
        const html = `
            <div class="d-flex mb-3" id="${id}">
                <div class="flex-shrink-0 bg-secondary text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                    <i class="bi bi-robot"></i>
                </div>
                <div class="ms-3 flex-grow-1">
                    <div class="card bg-light border-0 p-3 shadow-sm d-inline-block">
                        <div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div>
                        <span class="text-muted small">Thinking and searching documents...</span>
                    </div>
                </div>
            </div>
        `;
        chatMessages.insertAdjacentHTML("beforeend", html);
        return id;
    }

    function removeLoadingIndicator(id) {
        const element = document.getElementById(id);
        if (element) element.remove();
    }

    function scrollToBottom() {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
        );
    }
});