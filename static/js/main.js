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
            console.log('Response:', data);
            if (data.status === 'success') {
                addMessage(data.response.content, 'assistant');
                // Fetch evaluation metrics for the query
                await fetchEvaluateMetrics(message);
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
        if (sender === 'assistant') {
            // Render markdown to HTML for assistant messages
            contentDiv.innerHTML = marked.parse(text);
        } else {
            contentDiv.textContent = text;
        }
        
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

    // Allow sending message with Enter key (without Shift)
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
        }
    });

    async function fetchValidationMetrics() {
        try {
            const response = await fetch(`${API_BASE_URL}/validate`, {
                method: 'GET',
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Error fetching validation metrics:', errorData.detail);
                return;
            }

            const data = await response.json();
            console.log(data);
            const metricsDiv = document.getElementById('validationMetrics');
            metricsDiv.innerHTML = `
                <p><strong>Retrieval Metrics:</strong></p>
                <p>Precision: ${data.retrieval_metrics?.precision || 'N/A'}</p>
                <p>Recall: ${data.retrieval_metrics?.recall || 'N/A'}</p>
                <p>F1-Score: ${data.retrieval_metrics?.f1_score || 'N/A'}</p>
                <p><strong>LLM Metrics:</strong></p>
                <p>ROUGE-1: ${data.llm_metrics?.rouge1 || 'N/A'}</p>
                <p>ROUGE-L: ${data.llm_metrics?.rougeL || 'N/A'}</p>
                <p>BERTScore: ${data.llm_metrics?.bert_score || 'N/A'}</p>
            `;
        } catch (error) {
            console.error('Error:', error.message);
        }
    }

    // Fetch and display metrics from /validation/evaluate and /validation/validate endpoints
    async function fetchEvaluateMetrics(query) {
        try {
            const response = await fetch('/validation/evaluate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            if (!response.ok) throw new Error('Failed to fetch evaluation metrics');
            const data = await response.json();
            updateMetricsSection(data, 'Evaluation');
        } catch (error) {
            console.error('Evaluation metrics error:', error);
        }
    }

    async function fetchValidateMetrics(payload) {
        try {
            const response = await fetch('/validation/validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) throw new Error('Failed to fetch validation metrics');
            const data = await response.json();
            updateMetricsSection(data, 'Validation');
        } catch (error) {
            console.error('Validation metrics error:', error);
        }
    }

    function updateMetricsSection(data, label) {
        const metricsDiv = document.getElementById('validationMetrics');
        metricsDiv.innerHTML = `
            <p><strong>${label} - Retrieval Metrics:</strong></p>
            <p>Precision: ${data.retrieval_metrics?.precision ?? 'N/A'}</p>
            <p>Recall: ${data.retrieval_metrics?.recall ?? 'N/A'}</p>
            <p>F1-Score: ${data.retrieval_metrics?.f1_score ?? 'N/A'}</p>
            <p><strong>${label} - LLM Metrics:</strong></p>
            <p>ROUGE-1: ${data.llm_metrics?.rouge1 ?? 'N/A'}</p>
            <p>ROUGE-L: ${data.llm_metrics?.rougeL ?? 'N/A'}</p>
            <p>BERTScore: ${data.llm_metrics?.bert_score ?? 'N/A'}</p>
            ${data.latency !== undefined ? `<p>Latency: ${data.latency.toFixed(2)}s</p>` : ''}
        `;
    }

    // Call the function to fetch and display validation metrics
    fetchValidationMetrics();
});
