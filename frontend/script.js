document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://localhost:8000';
    const queryInput = document.getElementById('queryInput');
    const submitButton = document.getElementById('submitQuery');
    const refreshButton = document.getElementById('refreshCache');
    const responseDiv = document.getElementById('response');

    async function submitQuery() {
        try {
            const response = await fetch(`${API_BASE_URL}/agent`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: queryInput.value }),
            });
            
            const data = await response.json();
            if (response.ok) {
                responseDiv.textContent = data.response;
            } else {
                responseDiv.textContent = `Error: ${data.detail}`;
            }
        } catch (error) {
            responseDiv.textContent = `Error: ${error.message}`;
        }
    }

    async function refreshCache() {
        try {
            const response = await fetch(`${API_BASE_URL}/schedule`, {
                method: 'POST',
            });
            
            const data = await response.json();
            responseDiv.textContent = data.message;
        } catch (error) {
            responseDiv.textContent = `Error refreshing cache: ${error.message}`;
        }
    }

    submitButton.addEventListener('click', submitQuery);
    refreshButton.addEventListener('click', refreshCache);
});
