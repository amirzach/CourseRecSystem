const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const PORT = 5000; // Backend runs on this port

// Middleware
app.use(cors());
app.use(bodyParser.json());

// MongoDB connection
const MONGO_URI = "mongodb://localhost:27017/CourseRecDB";
mongoose.connect(MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).then(() => {
  console.log("Connected to MongoDB");
}).catch((err) => {
  console.error("Error connecting to MongoDB:", err);
});

// Define Mongoose Schemas
const GradeSchema = new mongoose.Schema({
  subject: String,
  grade: String,
});

const QuestionnaireSchema = new mongoose.Schema({
  grades: [GradeSchema], // Array of grade objects
  responses: Object, // Object to store questionnaire responses
});

const Grade = mongoose.model("Grade", GradeSchema);
const Questionnaire = mongoose.model("Questionnaire", QuestionnaireSchema);

// Routes for Grades
app.post("/grades", async (req, res) => {
  try {
    const grades = req.body; // Expecting an array of grades
    const savedGrades = await Grade.insertMany(grades);
    res.status(201).json(savedGrades);
  } catch (err) {
    res.status(500).json({ error: "Failed to save grades" });
  }
});

app.get("/grades", async (req, res) => {
  try {
    const grades = await Grade.find();
    res.status(200).json(grades);
  } catch (err) {
    res.status(500).json({ error: "Failed to fetch grades" });
  }
});

// Routes for Questionnaire
app.post("/questionnaire", async (req, res) => {
  try {
    const { grades, responses } = req.body; // Expecting grades and questionnaire responses
    const questionnaire = new Questionnaire({ grades, responses });
    const savedQuestionnaire = await questionnaire.save();
    res.status(201).json(savedQuestionnaire);
  } catch (err) {
    res.status(500).json({ error: "Failed to save questionnaire" });
  }
});

app.get("/questionnaire", async (req, res) => {
  try {
    const questionnaires = await Questionnaire.find();
    res.status(200).json(questionnaires);
  } catch (err) {
    res.status(500).json({ error: "Failed to fetch questionnaire data" });
  }
});

// Start the server
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));