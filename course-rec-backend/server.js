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
mongoose
  .connect(MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log("Connected to MongoDB");
  })
  .catch((err) => {
    console.error("Error connecting to MongoDB:", err.message);
  });

// Define Mongoose Schemas
const GradeSchema = new mongoose.Schema({
  subject: { type: String, required: true },
  grade: { type: String, required: true },
});

const QuestionnaireSchema = new mongoose.Schema({
  grades: [GradeSchema], // Array of grade objects
  responses: { type: Array, required: true }, // Array to store questionnaire responses
});

const Grade = mongoose.model("Grade", GradeSchema);
const Questionnaire = mongoose.model("Questionnaire", QuestionnaireSchema);

// Grade-to-value mapping
const gradeValues = {
  "A+": 4.3,
  A: 4,
  "A-": 3.7,
  "B+": 3.3,
  B: 3,
  "B-": 2.7,
  C: 2,
  D: 1,
  E: 0.5,
  F: 0,
};

// Course assignment rules
const assignCourses = (grades) => {
  const scores = {};
  for (const [subject, grade] of Object.entries(grades)) {
    scores[subject.toUpperCase()] = gradeValues[grade] || 0; // Convert grades to values
  }

  const recommendedCourses = [];

  if (scores["MATEMATIK"] >= 3.7 && scores["MATEMATIK TAMBAHAN"] >= 3.7 && scores["FIZIK"] >= 3) {
    recommendedCourses.push("Engineering");
  }
  if (scores["BIOLOGI"] >= 3.7 && scores["FIZIK"] >= 3 && scores["KIMIA"] >= 3) {
    recommendedCourses.push("Science");
  }
  if (scores["BIOLOGI"] >= 3.5 && scores["KIMIA"] >= 3.5) {
    recommendedCourses.push("Biotechnology");
  }
  if (scores["BIOLOGI"] >= 3 && scores["KIMIA"] >= 3 && scores["PENDIDIKAN SENI VISUAL"] >= 3) {
    recommendedCourses.push("Food Technology");
  }
  if (scores["PENDIDIKAN SENI VISUAL"] >= 3.7 && scores["BAHASA INGGERIS"] >= 3) {
    recommendedCourses.push("Fine Arts and Design");
  }
  if (scores["EKONOMI"] >= 3.5 || scores["PERNIAGAAN"] >= 3.5 || scores["PRINSIP PERAKAUNAN"] >= 3.5) {
    recommendedCourses.push("Commerce");
  }
  if (scores["MATEMATIK"] >= 3.5 && scores["BAHASA INGGERIS"] >= 3) {
    recommendedCourses.push("Information Technology");
  }
  if (scores["SEJARAH"] >= 3 && scores["BAHASA INGGERIS"] >= 3) {
    recommendedCourses.push("Law and Policing");
  }
  if (scores["PENDIDIKAN ISLAM"] >= 3.5 || scores["TASAWWUR ISLAM"] >= 3.5) {
    recommendedCourses.push("Islamic Studies and TESL");
  }
  if (scores["BAHASA MALAYSIA"] >= 3 && scores["BAHASA INGGERIS"] >= 3 && scores["PENDIDIKAN SENI VISUAL"] >= 3) {
    recommendedCourses.push("Arts and Media");
  }
  if (scores["BIOLOGI"] >= 3 && scores["MORAL"] >= 3) {
    recommendedCourses.push("Psychology and Health");
  }
  if (scores["BAHASA INGGERIS"] >= 3.5 && scores["PENDIDIKAN ISLAM"] >= 3.5) {
    recommendedCourses.push("Education");
  }
  if (scores["PERNIAGAAN"] >= 3.5 && scores["SEJARAH"] >= 3.5) {
    recommendedCourses.push("Travel and Hospitality");
  }

  // If no courses match, recommend 'General'
  if (recommendedCourses.length === 0) {
    recommendedCourses.push("General");
  }

  return recommendedCourses;
};

// Content-Based Filtering Logic
const refineRecommendation = (recommendedCourses, responses) => {
  const coursePreferences = {
    Engineering: ["Analytical", "Problem-solving", "Step-by-step", "Data", 5],
    Science: ["Analytical", "Curiosity about nature", "Step-by-step", "Data", 4],
    Biotechnology: ["Curiosity about nature", "Problem-solving", "Step-by-step", "Ideas", 4],
    "Food Technology": ["Practical", "Creativity in designing", "Hands-on", "Ideas", 3],
    "Fine Arts and Design": ["Creative", "Artistic talent", "Highly Creative", "Ideas", 5],
    Commerce: ["Business-minded", "Structured", "Working with numbers", "Data", 4],
    IT: ["Analytical", "Comfortable with technology", "Problem-solving", "Data", 4],
    Law: ["Highly Skilled", "Analyzing legal concepts", "Structured", "Ideas", 4],
    Psychology: ["Exploring human behavior", "People-oriented", "Dynamic", "Ideas", 5],
    Education: ["Teaching", "People-oriented", "Structured", "Ideas", 4],
    "Travel and Hospitality": ["Hospitality-related tasks", "People-oriented", "Dynamic", "Ideas", 4],
  };

  const scores = {};

  for (const course of recommendedCourses) {
    let score = 0;
    const preferences = coursePreferences[course];

    if (!preferences) continue;

    // Adjust score based on questionnaire responses
    if (responses.includes(preferences[0])) score += 1;
    if (responses.includes(preferences[1])) score += 1;
    if (responses.includes(preferences[2])) score += 1;
    if (responses.includes(preferences[3])) score += 1;
    if (responses[4] >= preferences[4]) score += 1;

    scores[course] = score;
  }

  // Return the course with the highest score
  return Object.keys(scores).reduce((a, b) => (scores[a] > scores[b] ? a : b), recommendedCourses[0] || null);
};

// Routes for Grades
app.post("/grades", async (req, res) => {
  try {
    const grades = req.body;
    const savedGrades = await Grade.insertMany(grades);
    res.status(201).json(savedGrades);
  } catch (err) {
    res.status(500).json({ error: "Failed to save grades", details: err.message });
  }
});

app.get("/grades", async (req, res) => {
  try {
    const grades = await Grade.find();
    res.status(200).json(grades);
  } catch (err) {
    res.status(500).json({ error: "Failed to fetch grades", details: err.message });
  }
});

// Route for Recommendations
app.post("/recommend", async (req, res) => {
  try {
    const grades = req.body; // Expecting a grades object
    const recommendedCourses = assignCourses(grades);
    res.status(200).json({ recommendedCourses });
  } catch (err) {
    res.status(500).json({ error: "Failed to generate recommendation", details: err.message });
  }
});

// Refined Recommendation Route
app.post("/refine", async (req, res) => {
  try {
    const { grades, responses } = req.body;

    // Generate initial recommendations
    const recommendedCourses = assignCourses(grades);

    // Save the questionnaire data to MongoDB
    const questionnaire = new Questionnaire({ grades, responses });
    await questionnaire.save();

    // Refine recommendation using questionnaire responses
    const refinedCourse = refineRecommendation(recommendedCourses, responses);

    res.status(200).json({ refinedCourse });
  } catch (err) {
    res.status(500).json({ error: "Failed to refine recommendation", details: err.message });
  }
});

// Start the server
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
