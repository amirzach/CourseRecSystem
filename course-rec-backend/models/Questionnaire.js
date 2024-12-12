const mongoose = require("mongoose");

const questionnaireSchema = new mongoose.Schema({
  grades: { type: Map, of: Number, required: true }, // Store grades as a map
  responses: { type: Map, of: String, required: true }, // Store responses as a map
  createdAt: { type: Date, default: Date.now }, // Timestamp
});

const Questionnaire = mongoose.model("Questionnaire", questionnaireSchema);

module.exports = Questionnaire;
