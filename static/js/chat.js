let ws;

function connectWebSocket() {
    ws = new WebSocket(`ws://${window.location.host}/ws/chat`);
    
    ws.onmessage = function(event) {
        appendMessage('bot', event.data);
    };

    ws.onclose = function() {
        setTimeout(connectWebSocket, 1000);
    };
}

function appendMessage(sender, message) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = message;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (message && ws.readyState === WebSocket.OPEN) {
        appendMessage('user', message);
        ws.send(message);
        input.value = '';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    connectWebSocket();

    document.getElementById('send-button').addEventListener('click', sendMessage);
    
    document.getElementById('user-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});