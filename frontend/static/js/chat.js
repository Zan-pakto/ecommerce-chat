// Chat state
let currentSessionId = null;
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');

// Initialize chat
async function initChat() {
    if (accessToken) {
        await createChatSession();
    }
}

// Create new chat session
async function createChatSession() {
    try {
        const response = await fetch('/api/chat/session', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            currentSessionId = data.session_id;
            addBotMessage('Hello! I\'m your shopping assistant. How can I help you today?');
        }
    } catch (error) {
        console.error('Error creating chat session:', error);
    }
}

// Send message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || !currentSessionId) return;
    
    // Add user message to chat
    addUserMessage(message);
    messageInput.value = '';
    
    try {
        const response = await fetch('/api/chat/message', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: currentSessionId,
                content: message
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            addBotMessage(data.bot_response);
        } else {
            addBotMessage('Sorry, I encountered an error. Please try again.');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        addBotMessage('Sorry, I encountered an error. Please try again.');
    }
}

// Add user message to chat
function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add bot message to chat
function addBotMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Scroll chat to bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Handle enter key in message input
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Load chat history
async function loadChatHistory() {
    if (!currentSessionId) return;
    
    try {
        const response = await fetch(`/api/chat/history/${currentSessionId}`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            chatMessages.innerHTML = '';
            data.messages.forEach(msg => {
                if (msg.is_bot) {
                    addBotMessage(msg.content);
                } else {
                    addUserMessage(msg.content);
                }
            });
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

// Reset chat session
async function resetChat() {
    if (!currentSessionId) return;
    
    try {
        const response = await fetch(`/api/chat/reset/${currentSessionId}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            currentSessionId = data.new_session_id;
            chatMessages.innerHTML = '';
            addBotMessage('Hello! I\'m your shopping assistant. How can I help you today?');
        }
    } catch (error) {
        console.error('Error resetting chat:', error);
    }
}

// Initialize chat when the page loads
document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    
    // Add welcome message
    addMessage("Welcome to our E-Commerce Assistant", 'bot');
    addMessage("I can help you find products and answer your questions. Here are some ways to search:\n\n" +
              "• Search for specific items (e.g., 'laptop', 't-shirt')\n" +
              "• Browse categories (e.g., 'electronics', 'clothing')\n" +
              "• Check prices and availability\n\n" +
              "What would you like to search for?", 'bot');
    
    // Handle message sending
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});

function addMessage(content, type) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = content.replace(/\n/g, '<br>');
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Initialize chat when user is authenticated
document.addEventListener('DOMContentLoaded', () => {
    if (accessToken) {
        initChat();
    }
}); 