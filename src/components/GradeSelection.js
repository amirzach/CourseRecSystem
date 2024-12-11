import axios from "axios";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles.css";

function GradeSelection({ onNext }) {
  const [grades, setGrades] = useState({
    "BAHASA MALAYSIA": '',
    "SEJARAH": '',
    "BAHASA INGGERIS": '',
    "MATEMATIK": '',
    "PENDIDIKAN ISLAM": '',
    "PENDIDIKAN MORAL": ''
  });

  const [additionalSubjects, setAdditionalSubjects] = useState({});
  const [newSubject, setNewSubject] = useState('');
  const [recommendation, setRecommendation] = useState(null);
  const navigate = useNavigate();

  const handleGradeChange = (e) => {
    const { name, value } = e.target;
    if (Object.keys(grades).includes(name)) {
      setGrades({ ...grades, [name]: value });
    } else {
      setAdditionalSubjects({ ...additionalSubjects, [name]: value });
    }
  };

  const handleAddSubject = () => {
    if (newSubject.trim() && !additionalSubjects[newSubject]) {
      setAdditionalSubjects({ ...additionalSubjects, [newSubject]: '' });
      setNewSubject('');
    }
  };

  const handleGetRecommendation = async () => {
    try {
      const allGrades = { ...grades, ...additionalSubjects };
      const response = await axios.post("http://localhost:5000/recommend", allGrades);
      setRecommendation(response.data);
    } catch (error) {
      console.error("Failed to get recommendation:", error);
    }
  };

  const handleSubmit = async () => {
    try {
      const allGrades = { ...grades, ...additionalSubjects };
      const data = Object.entries(allGrades).map(([subject, grade]) => ({
        subject,
        grade,
      }));
      await axios.post("http://localhost:5000/grades", data);
      onNext(data);
      navigate("/questionnaire");
    } catch (error) {
      console.error("Failed to save grades:", error);
    }
  };
  

  return (
    <div className="container">
      <h2>Course Recommender System</h2>
      <p>Enter your grade for each subject</p>

      <div className="subject-list">
        {Object.keys(grades).map((subject) => (
          <div key={subject} className="subject-item">
            <label className="subject-label">
              {subject.replace(/([A-Z])/g, " $1").toLowerCase()}
            </label>
            <select
              name={subject}
              value={grades[subject]}
              onChange={handleGradeChange}
              className="grade-select"
            >
              <option value="">Select</option>
              <option value="A+">A+</option>
              <option value="A">A</option>
              <option value="A-">A-</option>
              <option value="B+">B+</option>
              <option value="B">B</option>
              <option value="B-">B-</option>
              <option value="C">C</option>
              <option value="D">D</option>
              <option value="E">E</option>
              <option value="F">F</option>
            </select>
          </div>
        ))}

        {Object.keys(additionalSubjects).map((subject) => (
          <div key={subject} className="subject-item">
            <label className="subject-label">{subject}</label>
            <select
              name={subject}
              value={additionalSubjects[subject]}
              onChange={handleGradeChange}
              className="grade-select"
            >
              <option value="">Select</option>
              <option value="A+">A+</option>
              <option value="A">A</option>
              <option value="A-">A-</option>
              <option value="B+">B+</option>
              <option value="B">B</option>
              <option value="B-">B-</option>
              <option value="C">C</option>
              <option value="D">D</option>
              <option value="E">E</option>
              <option value="F">F</option>
            </select>
          </div>
        ))}
      </div>

      <div className="add-subject-container">
        <input
          type="text"
          placeholder="Add a new subject"
          value={newSubject}
          onChange={(e) => setNewSubject(e.target.value)}
          className="add-subject-input"
        />
        <button onClick={handleAddSubject} className="add-subject-button">
          Add Subject
        </button>
      </div>

      {recommendation && (
        <div className="recommendation-result">
          <h3>Recommended Courses:</h3>
          <ul>
          {recommendation.recommendedCourses.map((course, index) => (
              <li key={index}>{course}</li>
            ))}
          </ul>
          <p>Accuracy: {recommendation.accuracy?.toFixed(2) || 'N/A'}%</p>
        </div>
      )}

      <button onClick={handleGetRecommendation} className="recommend-button">
        Get Recommendation
      </button>

      <button onClick={handleSubmit} className="submit-button">
        Next
      </button>
    </div>
  );
}

export default GradeSelection;
