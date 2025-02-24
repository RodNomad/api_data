document.getElementById('chatForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const systemInput = document.getElementById('systemInput').value;
    const userInput = document.getElementById('userInput').value;
    const answerInput = document.getElementById('answerInput').value;
    const chatMessages = document.getElementById('chatMessages');

    // Adicionar mensagens ao chat
    if (systemInput) {
        chatMessages.innerHTML += `<div class="system-message">Prompt: ${systemInput}</div>`;
    }
    if (userInput) {
        chatMessages.innerHTML += `<div class="user-message">User: ${userInput}</div>`;
    }
    if (answerInput) {
        chatMessages.innerHTML += `<div class="answer-message">AI: ${answerInput}</div>`;
    }

    // Limpar os campos
    document.getElementById('systemInput').value = '';
    document.getElementById('userInput').value = '';
    document.getElementById('answerInput').value = '';

    // Scroll para o final
    chatMessages.scrollTop = chatMessages.scrollHeight;
});