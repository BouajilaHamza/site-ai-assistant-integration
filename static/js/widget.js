// Lightweight Chat Widget
(function () {
  if (window.MoznChatWidgetLoaded) return;
  window.MoznChatWidgetLoaded = true;

  // Create chat button
  var chatBtn = document.createElement('div');
  chatBtn.innerText = '💬 Chat';
  chatBtn.style.position = 'fixed';
  chatBtn.style.bottom = '24px';
  chatBtn.style.right = '24px';
  chatBtn.style.background = '#007bff';
  chatBtn.style.color = '#fff';
  chatBtn.style.padding = '12px 20px';
  chatBtn.style.borderRadius = '24px';
  chatBtn.style.cursor = 'pointer';
  chatBtn.style.zIndex = 9999;
  chatBtn.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
  chatBtn.style.fontFamily = 'sans-serif';

  // Create chat window
  var chatWindow = document.createElement('div');
  chatWindow.style.position = 'fixed';
  chatWindow.style.bottom = '70px';
  chatWindow.style.right = '24px';
  chatWindow.style.width = '320px';
  chatWindow.style.height = '400px';
  chatWindow.style.background = '#fff';
  chatWindow.style.border = '1px solid #ddd';
  chatWindow.style.borderRadius = '12px';
  chatWindow.style.boxShadow = '0 2px 16px rgba(0,0,0,0.18)';
  chatWindow.style.display = 'none';
  chatWindow.style.flexDirection = 'column';
  chatWindow.style.overflow = 'hidden';
  chatWindow.style.zIndex = 10000;
  chatWindow.style.fontFamily = 'sans-serif';

  // Chat header
  var header = document.createElement('div');
  header.innerText = 'Mozn AI Assistant';
  header.style.background = '#007bff';
  header.style.color = '#fff';
  header.style.padding = '12px';
  header.style.fontWeight = 'bold';
  header.style.textAlign = 'center';
  chatWindow.appendChild(header);

  // Chat messages area
  var messages = document.createElement('div');
  messages.style.flex = '1';
  messages.style.padding = '12px';
  messages.style.overflowY = 'auto';
  chatWindow.appendChild(messages);

  // Chat input area
  var inputArea = document.createElement('div');
  inputArea.style.display = 'flex';
  inputArea.style.borderTop = '1px solid #eee';
  var input = document.createElement('input');
  input.type = 'text';
  input.placeholder = 'Type your message...';
  input.style.flex = '1';
  input.style.padding = '10px';
  input.style.border = 'none';
  input.style.outline = 'none';
  var sendBtn = document.createElement('button');
  sendBtn.innerText = 'Send';
  sendBtn.style.background = '#007bff';
  sendBtn.style.color = '#fff';
  sendBtn.style.border = 'none';
  sendBtn.style.padding = '0 16px';
  sendBtn.style.cursor = 'pointer';
  inputArea.appendChild(input);
  inputArea.appendChild(sendBtn);
  chatWindow.appendChild(inputArea);

  // Add to DOM
  document.body.appendChild(chatBtn);
  document.body.appendChild(chatWindow);

  // Toggle chat window
  chatBtn.onclick = function () {
    chatWindow.style.display = chatWindow.style.display === 'none' ? 'flex' : 'none';
  };

  // Send message
  function appendMessage(text, from) {
    var msg = document.createElement('div');
    msg.innerText = text;
    msg.style.margin = '8px 0';
    msg.style.textAlign = from === 'user' ? 'right' : 'left';
    msg.style.color = from === 'user' ? '#007bff' : '#222';
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
  }

  function sendMessage() {
    var text = input.value.trim();
    if (!text) return;
    appendMessage(text, 'user');
    input.value = '';
    // Call backend API
    fetch('https://YOUR_BACKEND_URL/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    })
      .then(r => r.json())
      .then(data => {
        appendMessage(data.response || 'No response', 'bot');
      })
      .catch(() => {
        appendMessage('Error contacting server.', 'bot');
      });
  }

  sendBtn.onclick = sendMessage;
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') sendMessage();
  });
})();
