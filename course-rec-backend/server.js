const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());

const MONGO_URI = "mongodb://localhost:27017/CourseRecDB";
mongoose
  .connect(MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.error("Error connecting to MongoDB:", err));

const GradeSchema = new mongoose.Schema({
  subject: String,
  grade: String,
});

const QuestionnaireSchema = new mongoose.Schema({
  grades: [GradeSchema],
  responses: Object,
});

const Grade = mongoose.model("Grade", GradeSchema);
const Questionnaire = mongoose.model("Questionnaire", QuestionnaireSchema);

app.post("/questionnaire", async (req, res) => {
  try {
    const { grades, responses } = req.body;

    if (!grades || !responses) {
      return res.status(400).json({ error: "Grades and responses are required." });
    }

    const questionnaire = new Questionnaire({ grades, responses });
    const savedQuestionnaire = await questionnaire.save();

    res.status(201).json(savedQuestionnaire);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to save questionnaire." });
  }
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
