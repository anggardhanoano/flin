document.addEventListener("DOMContentLoaded", () => {
  const flinChat = document.getElementById("chat-toggle");
  const closeChat = document.getElementById("close-chat");
  const chatContainer = document.getElementById("chat-container");
  const chatMessages = document.getElementById("chat-messages");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");

  const chatHistory = [];

  flinChat.addEventListener("click", () => {
    chatContainer.classList.remove("collapsed");
    flinChat.classList.add("hidden");
    userInput.focus();
  });

  closeChat.addEventListener("click", () => {
    chatContainer.classList.add("collapsed");
    flinChat.classList.remove("hidden");
  });

  function addMessage(message, isUser) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.classList.add(isUser ? "user" : "bot");

    const messageContent = document.createElement("div");
    messageContent.classList.add("message-content");
    messageContent.textContent = message;

    messageElement.appendChild(messageContent);
    chatMessages.appendChild(messageElement);

    chatMessages.scrollTop = chatMessages.scrollHeight;

    chatHistory.push({
      text: message,
      isUser: isUser,
    });
  }

  function showTypingIndicator() {
    const indicator = document.createElement("div");
    indicator.classList.add("typing-indicator");
    indicator.id = "typing-indicator";

    for (let i = 0; i < 5; i++) {
      const dot = document.createElement("span");
      indicator.appendChild(dot);
    }

    chatMessages.appendChild(indicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function removeTypingIndicator() {
    const indicator = document.getElementById("typing-indicator");
    if (indicator) {
      indicator.remove();
    }
  }

  async function sendMessage(message) {
    addMessage(message, true);

    userInput.value = "";

    showTypingIndicator();

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message, chatHistory }),
      });

      const data = await response.json();

      removeTypingIndicator();

      if (data.response) {
        addMessage(data.response, false);
      } else if (data.error) {
        addMessage("Sorry, I encountered an error. Please try again.", false);
      }
    } catch (error) {
      console.error("Error sending message:", error);

      removeTypingIndicator();

      addMessage("Sorry, I encountered an error. Please try again.", false);
    }
  }

  sendButton.addEventListener("click", () => {
    const message = userInput.value.trim();
    if (message) {
      sendMessage(message);
    }
  });

  userInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      const message = userInput.value.trim();
      if (message) {
        sendMessage(message);
      }
    }
  });

  userInput.focus();
});
