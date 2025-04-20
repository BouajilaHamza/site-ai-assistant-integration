document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatContainer = document.getElementById('chat-container');
    const submitButton = chatForm.querySelector('button[type="submit"]');
    let isProcessing = false;

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (isProcessing) return;

        const message = messageInput.value.trim();
        if (!message) return;

        try {
            isProcessing = true;
            toggleLoadingState(true);
            
            // Add user message to chat
            addMessage(message, 'user');
            messageInput.value = '';

            // Send message to backend
            const response = await fetch('agents/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.status === 'success') {
                addMessage(data.response, 'assistant');
            } else {
                throw new Error('Response was not successful');
            }

        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your request.', 'assistant', true);
        } finally {
            isProcessing = false;
            toggleLoadingState(false);
        }
    });

    function addMessage(text, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        if (isError) messageDiv.classList.add('error-message');
        
        // Create message content
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.textContent = text;
        
        messageDiv.appendChild(contentDiv);
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function toggleLoadingState(isLoading) {
        submitButton.disabled = isLoading;
        submitButton.innerHTML = isLoading ? 
            '<i class="fas fa-spinner fa-spin"></i>' : 
            '<i class="fas fa-paper-plane"></i>';
        messageInput.disabled = isLoading;
    }

    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});
