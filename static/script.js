const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatArea = document.getElementById('chatArea');

chatForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const userMessage = userInput.value.trim();
    if (userMessage === '') return;

    displayMessage(userMessage, 'user');

    const response = await fetch('/send-message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    });

    const responseData = await response.json();
    displayMessage(responseData.reply, 'gemini');

    userInput.value = '';
});

function displayMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.innerHTML = `<p>${message}</p>`;
    chatArea.appendChild(messageElement);
    chatArea.scrollTop = chatArea.scrollHeight; // Scroll automaticamente para a última mensagem
}