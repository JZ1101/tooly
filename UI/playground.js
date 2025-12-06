// Playground functionality
class Web3Playground {
    constructor() {
        this.apiUrl = 'http://localhost:8000/api/chat';
        this.messagesContainer = document.getElementById('messages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.statusIndicator = document.getElementById('status');
        
        this.init();
        this.checkBackendStatus();
    }
    
    init() {
        // Send button click
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Enter key to send
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Example query clicks
        document.querySelectorAll('.example-query').forEach(query => {
            query.addEventListener('click', () => {
                this.messageInput.value = query.dataset.query;
                this.sendMessage();
            });
        });
        
        // Auto-focus input
        this.messageInput.focus();
    }
    
    async checkBackendStatus() {
        try {
            const response = await fetch('http://localhost:8000/health');
            if (response.ok) {
                this.updateStatus('online', 'Online');
            } else {
                this.updateStatus('offline', 'Backend Error');
            }
        } catch (error) {
            this.updateStatus('offline', 'Offline (Start backend)');
        }
    }
    
    updateStatus(status, text) {
        if (!this.statusIndicator) return;
        this.statusIndicator.className = `status-pill ${status}`;
        this.statusIndicator.textContent = text;
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // Add user message
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        
        // Disable input while processing
        this.setLoading(true);
        
        try {
            // Add thinking indicator
            const thinkingId = this.addThinkingMessage();
            
            // Send to backend
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: message,
                    session_id: this.generateSessionId()
                })
            });
            
            // Remove thinking message
            this.removeMessage(thinkingId);
            
            if (!response.ok) {
                throw new Error(`Backend error: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Add agent response
            this.addMessage(data.response, 'agent', data.success);
            
        } catch (error) {
            // Remove thinking message if it exists
            const thinking = document.querySelector('[data-thinking]');
            if (thinking) thinking.remove();
            
            // Add error message
            this.addMessage(
                this.getErrorMessage(error),
                'agent',
                false
            );
        }
        
        this.setLoading(false);
    }
    
    addMessage(content, sender, success = true) {
        const messageId = 'msg-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.id = messageId;
        
        if (sender === 'agent' && !success) {
            messageDiv.classList.add('error');
        }
        
        messageDiv.innerHTML = this.formatMessage(content, sender);
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        return messageId;
    }
    
    addThinkingMessage() {
        const messageId = 'thinking-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message agent';
        messageDiv.id = messageId;
        messageDiv.setAttribute('data-thinking', 'true');
        messageDiv.innerHTML = '<div class="thinking">🧠 Processing your request...</div>';
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        return messageId;
    }
    
    removeMessage(messageId) {
        const element = document.getElementById(messageId);
        if (element) {
            element.remove();
        }
    }
    
    formatMessage(content, sender) {
        if (sender === 'user') {
            return content;
        }
        
        // Format agent messages with better display
        let formatted = content;
        
        // Convert newlines to breaks
        formatted = formatted.replace(/\n/g, '<br>');
        
        // Bold important text
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Format code blocks
        formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Add some styling for common patterns
        formatted = formatted.replace(/(\$[\d,]+\.?\d*)/g, '<span style="color: #4caf50; font-weight: 600;">$1</span>');
        formatted = formatted.replace(/(\d+\.?\d*\s*ETH)/g, '<span style="color: #667eea; font-weight: 600;">$1</span>');
        
        return formatted;
    }
    
    getErrorMessage(error) {
        if (error.message.includes('Failed to fetch')) {
            return `
                🚫 <strong>Connection Error</strong><br><br>
                Can't connect to the backend server. Make sure you have:
                <br><br>
                1. Started the backend: <code>python main.py</code><br>
                2. Backend running on <code>http://localhost:8000</code><br>
                3. CORS enabled for frontend requests<br><br>
                <em>Check the console for more details.</em>
            `;
        } else if (error.message.includes('503')) {
            return `
                ⚠️ <strong>Agent Unavailable</strong><br><br>
                The UserAgent is not properly configured. This usually means:
                <br><br>
                • Missing <code>ANTHROPIC_API_KEY</code> in your <code>.env</code> file<br>
                • Invalid API key configuration<br><br>
                <em>Please check your environment setup.</em>
            `;
        } else {
            return `
                ❌ <strong>Error</strong><br><br>
                ${error.message}<br><br>
                <em>Please try again or check your configuration.</em>
            `;
        }
    }
    
    setLoading(loading) {
        this.sendBtn.disabled = loading;
        this.messageInput.disabled = loading;
        
        if (loading) {
            this.sendBtn.textContent = 'Sending...';
            this.messagesContainer.classList.add('loading');
        } else {
            this.sendBtn.textContent = 'Send';
            this.messagesContainer.classList.remove('loading');
        }
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    generateSessionId() {
        return 'session-' + Math.random().toString(36).substr(2, 9);
    }
}

// Initialize playground when page loads
document.addEventListener('DOMContentLoaded', () => {
    new Web3Playground();
    
    // Add some keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K to focus input
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            document.getElementById('messageInput').focus();
        }
        
        // Escape to blur input
        if (e.key === 'Escape') {
            document.getElementById('messageInput').blur();
        }
    });
});

// Add some utility functions for testing
window.testPlayground = {
    sendTestMessage: (message) => {
        const input = document.getElementById('messageInput');
        input.value = message;
        document.getElementById('sendBtn').click();
    },
    
    clearChat: () => {
        const messages = document.getElementById('messages');
        messages.innerHTML = `
            <div class="message agent">
                👋 Chat cleared! I'm ready to help with your Web3 questions.
            </div>
        `;
    }
};