const fs = require("fs");
const path = require("path");

const knowledgePath = path.join(__dirname, "../knowledge/knowledge.json");

/**
 * Get the knowledge base content
 * @returns {string} Combined knowledge as a string
 */
function getKnowledge() {
  try {
    if (!fs.existsSync(knowledgePath)) {
      const defaultKnowledge = {
        entries: [
          {
            question: "Apa itu Program Dana Talangan dari FLIN?",
            answer:
              "Program Dana Talangan adalah **layanan konsolidasi utang** yang meringankan beban finansial dengan menggabungkan beberapa utang menjadi satu cicilan tetap dan satu bunga per bulan [1]. Dana talangan akan disalurkan langsung ke berbagai debitur dan/atau bank terkait untuk melunasi semua utang Anda [1, 2].",
          },
        ],
      };

      const dir = path.dirname(knowledgePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }

      fs.writeFileSync(
        knowledgePath,
        JSON.stringify(defaultKnowledge, null, 2)
      );
    }

    const knowledgeData = JSON.parse(fs.readFileSync(knowledgePath, "utf8"));

    return knowledgeData.entries
      .map((entry) => `${entry.question}:\n${entry.answer}`)
      .join("\n\n");
  } catch (error) {
    console.error("Error:", error);
    return "No knowledge available.";
  }
}

module.exports = { getKnowledge };
