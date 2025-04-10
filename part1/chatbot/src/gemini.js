const { GoogleGenerativeAI } = require("@google/generative-ai");

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

/**
 * Generate a response using Gemini with custom knowledge as context
 * @param {string} message - User's message
 * @param {string} knowledge - Custom knowledge to provide as context
 * @param {Array} chatHistory - Previous chat messages
 * @returns {Promise<string>} - Generated response
 */
async function generateResponse(message, knowledge, chatHistory = []) {
  try {
    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

    const formattedHistory = chatHistory.map((msg) => ({
      role: msg.isUser ? "user" : "model",
      parts: [{ text: msg.text }],
    }));

    const chat = model.startChat({
      history: formattedHistory,
      generationConfig: {
        maxOutputTokens: 1000,
        temperature: 0.7,
      },
    });

    const promptWithContext = `
    I want you to answer the following question based ONLY on the knowledge provided below.
    If the answer cannot be found in the provided knowledge, please answer you don't have any information about it.
    
    KNOWLEDGE:
    ${knowledge}
    
    USER QUESTION: ${message}
    `;

    // Send the prompt to Gemini
    const result = await chat.sendMessage(promptWithContext);
    return result.response.text();
  } catch (error) {
    console.error("Error response from Gemini:", error);
    throw error;
  }
}

module.exports = { generateResponse };
