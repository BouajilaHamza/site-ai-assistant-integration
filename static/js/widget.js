// Lightweight Chat Widget
(function () {
  if (window.MoznChatWidgetLoaded) return;
  window.MoznChatWidgetLoaded = true;

  // Create chat button (floating, with icon)
  var chatBtn = document.createElement('div');
  chatBtn.innerHTML = '<svg width="22" height="22" style="vertical-align:middle;margin-right:8px;" fill="#fff" viewBox="0 0 24 24"><path d="M12 3C6.477 3 2 6.797 2 11c0 1.61.672 3.104 1.82 4.36-.13.63-.47 1.97-.7 2.82-.12.41.28.78.7.66.86-.26 2.23-.7 2.86-.91C8.36 18.61 10.12 19 12 19c5.523 0 10-3.797 10-8s-4.477-8-10-8zm0 14c-1.7 0-3.32-.34-4.62-.97l-.32-.16-2.13.68.66-2.13-.19-.32C4.34 13.32 4 12.17 4 11c0-3.866 4.03-7 9-7s9 3.134 9 7-4.03 7-9 7zm-4-7a1 1 0 1 1 2 0 1 1 0 0 1-2 0zm4 0a1 1 0 1 1 2 0 1 1 0 0 1-2 0zm4 0a1 1 0 1 1 2 0 1 1 0 0 1-2 0z"/></svg>Your Site Companion';
  chatBtn.style.position = 'fixed';
  chatBtn.style.bottom = '32px';
  chatBtn.style.right = '32px';
  chatBtn.style.background = 'linear-gradient(90deg, #007bff 60%, #00c6ff 100%)';
  chatBtn.style.color = '#fff';
  chatBtn.style.padding = '14px 28px';
  chatBtn.style.borderRadius = '32px';
  chatBtn.style.cursor = 'pointer';
  chatBtn.style.zIndex = 9999;
  chatBtn.style.boxShadow = '0 4px 16px rgba(0,0,0,0.18)';
  chatBtn.style.fontFamily = 'Inter,Segoe UI,sans-serif';
  chatBtn.style.fontWeight = '600';
  chatBtn.style.fontSize = '1rem';
  chatBtn.style.transition = 'box-shadow 0.2s';
  chatBtn.onmouseenter = () => chatBtn.style.boxShadow = '0 8px 24px rgba(0,0,0,0.22)';
  chatBtn.onmouseleave = () => chatBtn.style.boxShadow = '0 4px 16px rgba(0,0,0,0.18)';

  // Create chat window
  var chatWindow = document.createElement('div');
  chatWindow.style.position = 'fixed';
  chatWindow.style.bottom = '90px';
  chatWindow.style.right = '32px';
  chatWindow.style.width = '350px';
  chatWindow.style.height = '480px';
  chatWindow.style.background = '#fff';
  chatWindow.style.border = '1.5px solid #e3e8ee';
  chatWindow.style.borderRadius = '18px';
  chatWindow.style.boxShadow = '0 8px 32px rgba(0,0,0,0.18)';
  chatWindow.style.display = 'none';
  chatWindow.style.flexDirection = 'column';
  chatWindow.style.overflow = 'hidden';
  chatWindow.style.zIndex = 10000;
  chatWindow.style.fontFamily = 'Inter,Segoe UI,sans-serif';

  // Chat header with close button
  var header = document.createElement('div');
  header.style.background = 'linear-gradient(90deg, #007bff 60%, #00c6ff 100%)';
  header.style.color = '#fff';
  header.style.padding = '16px 18px';
  header.style.fontWeight = 'bold';
  header.style.fontSize = '1.1rem';
  header.style.display = 'flex';
  header.style.alignItems = 'center';
  header.style.justifyContent = 'space-between';

  var headerTitle = document.createElement('span');
  headerTitle.innerText = 'Site AI Assistant';
  header.appendChild(headerTitle);

  var closeBtn = document.createElement('span');
  closeBtn.innerHTML = '&times;';
  closeBtn.style.cursor = 'pointer';
  closeBtn.style.fontSize = '1.5rem';
  closeBtn.style.marginLeft = '12px';
  closeBtn.onclick = function () {
    chatWindow.style.display = 'none';
  };
  header.appendChild(closeBtn);

  chatWindow.appendChild(header);

  // Chat messages area
  var messages = document.createElement('div');
  messages.style.flex = '1';
  messages.style.padding = '16px';
  messages.style.overflowY = 'auto';
  messages.style.background = '#f7fafd';
  chatWindow.appendChild(messages);

  // Chat input area
  var inputArea = document.createElement('div');
  inputArea.style.display = 'flex';
  inputArea.style.borderTop = '1px solid #e3e8ee';
  inputArea.style.background = '#fff';
  inputArea.style.padding = '10px 12px';

  var input = document.createElement('input');
  input.type = 'text';
  input.placeholder = 'Type your message...';
  input.style.flex = '1';
  input.style.padding = '10px 12px';
  input.style.border = '1px solid #e3e8ee';
  input.style.borderRadius = '8px';
  input.style.outline = 'none';
  input.style.fontSize = '1rem';
  input.style.background = '#f9fbfc';
  input.style.marginRight = '8px';

  var sendBtn = document.createElement('button');
  sendBtn.innerText = 'Send';
  sendBtn.style.background = 'linear-gradient(90deg, #007bff 60%, #00c6ff 100%)';
  sendBtn.style.color = '#fff';
  sendBtn.style.border = 'none';
  sendBtn.style.borderRadius = '8px';
  sendBtn.style.padding = '0 22px';
  sendBtn.style.fontWeight = 'bold';
  sendBtn.style.fontSize = '1rem';
  sendBtn.style.cursor = 'pointer';
  sendBtn.style.transition = 'background 0.2s';
  sendBtn.onmouseenter = () => sendBtn.style.background = 'linear-gradient(90deg, #0056b3 60%, #00aaff 100%)';
  sendBtn.onmouseleave = () => sendBtn.style.background = 'linear-gradient(90deg, #007bff 60%, #00c6ff 100%)';

  inputArea.appendChild(input);
  inputArea.appendChild(sendBtn);
  chatWindow.appendChild(inputArea);

  // Add to DOM
  document.body.appendChild(chatBtn);
  document.body.appendChild(chatWindow);

  // Toggle chat window
  chatBtn.onclick = function () {
    chatWindow.style.display = chatWindow.style.display === 'none' ? 'flex' : 'none';
    if (chatWindow.style.display === 'flex') input.focus();
  };

  // Helper: Render markdown and newlines to HTML
  function renderMarkdown(text) {
    let html = text
      .replace(/</g, "&lt;").replace(/>/g, "&gt;") // Escape HTML
      .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')     // Bold
      .replace(/\*(.*?)\*/g, '<i>$1</i>')         // Italic
      .replace(/`([^`]+)`/g, '<code>$1</code>')   // Inline code
      .replace(/\n/g, '<br>');                    // Newlines
    return html;
  }

  function appendMessage(text, from) {
    var msg = document.createElement('div');
    msg.style.margin = '10px 0';
    msg.style.maxWidth = '85%';
    msg.style.wordBreak = 'break-word';
    msg.style.padding = '10px 14px';
    msg.style.borderRadius = '14px';
    msg.style.fontSize = '1rem';
    msg.style.boxShadow = '0 1px 4px rgba(0,0,0,0.04)';
    if (from === 'user') {
      msg.style.background = 'linear-gradient(90deg, #e3f0ff 60%, #e0f7fa 100%)';
      msg.style.color = '#007bff';
      msg.style.alignSelf = 'flex-end';
      msg.style.marginLeft = 'auto';
      msg.innerText = text;
    } else {
      msg.style.background = '#fff';
      msg.style.color = '#222';
      msg.style.alignSelf = 'flex-start';
      msg.style.marginRight = 'auto';
      msg.innerHTML = renderMarkdown(text);
    }
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
  }

  function sendMessage() {
    var text = input.value.trim();
    if (!text) return;
    appendMessage(text, 'user');
    input.value = '';
    sendBtn.disabled = true;
    sendBtn.innerText = '...';
    // Call backend API
    fetch('http://127.0.0.1:8000/agents/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    })
      .then(r => r.json())
      .then(data => {
        appendMessage(data.response.content || 'No response', 'bot');
      })
      .catch(() => {
        appendMessage('Error contacting server.', 'bot');
      })
      .finally(() => {
        sendBtn.disabled = false;
        sendBtn.innerText = 'Send';
      });
  }

  sendBtn.onclick = sendMessage;
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') sendMessage();
  });
})();
