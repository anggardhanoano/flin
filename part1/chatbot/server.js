require("dotenv").config();
const express = require("express");
const cors = require("cors");
const path = require("path");
const { generateResponse } = require("./src/gemini");
const { getKnowledge } = require("./src/knowledge");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

app.post("/api/chat", async (req, res) => {
  try {
    const { message, chatHistory = [] } = req.body;

    const knowledge = getKnowledge();

    const response = await generateResponse(message, knowledge, chatHistory);

    res.json({ response });
  } catch (error) {
    console.error("Error chat request:", error);
    res.status(500).json({ error: "Failed to generate response" });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
