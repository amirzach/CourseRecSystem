import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles.css";
import axios from 'axios';

function Questionnaire({ grades, onSubmit }) {
  const [answers, setAnswers] = useState({});
  const [recommendation, setRecommendation] = useState(null);
  const navigate = useNavigate();

  const questions = [
    {
      type: "multipleChoice",
      question: "Do you consider yourself more creative, analytical, or practical?",
      options: ["1-Creative", "2-Analytical", "3-Practical"],
    },
    {
      type: "multipleChoice",
      question: "Which set of skills or interests best describes you?",
      options: [
        "1. Problem-solving, logical thinking, and an interest in how things work.",
        "2. Curiosity about nature, scientific research, and exploring how the world works.",
        "3. Interest in biology, innovation, and working on solutions to health or environmental issues.",
        "4. Creativity in designing or making things, especially in food or other practical applications.",
        "5. Artistic talent, creativity, and a passion for visual expression.",
        "6. Business-minded, with an interest in economics, finance, or managing projects.",
        "7. Interest in technology, computers, and solving problems using logical approaches.",
        "8. Passion for history, law, or making a difference in society through governance or public service.",
        "9. Interest in teaching, religious studies, or exploring cultural traditions.",
        "10. Communication skills, creativity, and a passion for media, storytelling, or the arts.",
        "11. Interest in understanding human behavior, empathy, and helping others.",
        "12. Enjoy working with people, sharing knowledge, and guiding others.",
        "13. Love for exploring new places, cultures, and organizing travel experiences.",
      ],
    },
    {
      type: "multipleChoice",
      question: "How do you approach solving problems: step-by-step or intuitively?",
      options: ["1-Step-by-step", "2-Intuitively"],
    },
    {
      type: "multipleChoice",
      question: "Are you more comfortable working with data, people, or ideas?",
      options: ["1-Data", "2-People", "3-Ideas"],
    },
    {
      type: "multipleChoice",
      question: "How would you describe your learning style: visual, auditory, reading/writing, or kinesthetic?",
      options: ["1-Visual", "2-Auditory", "3-reading/writing","4-kinesthetic"],
    },    
    {
      type: "radioScale",
      question: "How confident are you in your mathematical skills?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Not Confident", "Very Confident"],
    },
    {
      type: "radioScale",
      question: "How would you rate your ability to understand and apply specific scientific concepts like biology, physics, and chemistry?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Poor", "Excellent"],
    },
    {
      type: "radioScale",
      question: "How proficient are you in solving additional mathematics problems?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Not Proficient", "Very Proficient"],
    },
    {
      type: "radioScale",
      question: "How would you rate your artistic or visual design abilities?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Very Weak", "Very Strong"],
    },
    {
      type: "radioScale",
      question: "How comfortable are you working on experiments or lab-based tasks?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Very Uncomfortable", "Very Comfortable"],
    },
    {
      type: "radioScale",
      question: "How would you rate your understanding of economics, accounting, or business concepts?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Very Weak", "Very Strong"],
    },
    {
      type: "radioScale",
      question: "How confident are you in your command of the English language, both written and spoken?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Not Confident", "Very Confident"],
    },
    {
      type: "radioScale",
      question: "How skilled are you at analyzing historical or legal concepts?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Not Skilled", "Highly Skilled"],
    },
    {
      type: "radioScale",
      question: "How strong is your grasp of Islamic Studies or moral concepts?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Very Weak", "Very Strong"],
    },
    {
      type: "radioScale",
      question: "How well do you communicate in Bahasa Malaysia?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Poorly", "Fluently"],
    },
    {
      type: "radioScale",
      question: "How much do you enjoy solving complex problems?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Not At All", "Very Much"],
    },
    {
      type: "radioScale",
      question: "How do you prefer hands-on, practical work or theoretical study?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Entirely theoretical", "Entirely Practical"],
    },
    {
      type: "radioScale",
      question: "How creative are you in coming up with new ideas or designs?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Not Creative", "Highly Creative"],
    },
    {
      type: "radioScale",
      question: "How comfortable are you working with technology and learning new software tools?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Not Comfortable", "Very Comfortable"],
    },
    {
      type: "radioScale",
      question: "Do you enjoy working with numbers and financial data?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Not At All", "Very Much"],
    },
    {
      type: "radioScale",
      question: "How much do you enjoy exploring human behavior or psychological concepts?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Not At All", "Very Much"],
    },
    {
      type: "radioScale",
      question: "Do you enjoy planning trips, learning about different cultures, or engaging in hospitality-related tasks?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Not At All", "Very Much"],
    },
    {
      type: "radioScale",
      question: "How confident are you in your ability to lead and manage projects or teams?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Not Confident", "Very Confident"],
    },
    {
      type: "radioScale",
      question: "Do you prefer working in structured environments or dynamic, creative spaces?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Entirely structured", "Entirely dynamic"],
    },
    {
      type: "radioScale",
      question: "How interested are you in contributing to society through teaching or educational programs?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Not At All", "Very Interested"],
    },
  ];  

  const handleChange = (index, value) => {
    setAnswers({ ...answers, [index]: parseInt(value) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Log answers to debug
      console.log("Submitting answers:", answers);
      
      const response = await axios.post('/api/recommend', { answers });
      
      // Log the response data to debug
      console.log("Response from server:", response);

      setRecommendation(response.data.recommendation);

      // Submit the recommended course to the server
      await axios.post('/api/submit-course', { recommendedCourse: response.data.recommendation });

    } catch (error) {
      // Log detailed error to help debug
      console.error("Error submitting answers:", error);
      if (error.response) {
        console.error("Response error:", error.response.data);
      } else if (error.request) {
        console.error("Request error:", error.request);
      } else {
        console.error("General error:", error.message);
      }
    }
  };

  return (
    <div className="container">
      <h2>Course Recommender System</h2>
      <form onSubmit={handleSubmit}>
        {questions.map((q, index) => (
          <div key={index} className="question">
            <p>{q.question}</p>
            {q.type === "multipleChoice" ? (
              <div className="vertical-options">
                {q.options.map((option, i) => (
                  <label key={i} className="radio-label">
                    <input
                      type="radio"
                      name={`question-${index}`}
                      value={i + 1}
                      onChange={(e) => handleChange(index, e.target.value)}
                      required
                    />
                    {option}
                  </label>
                ))}
              </div>
            ) : (
              <div className="horizontal-options">
                <span className="scale-label">{q.labels[0]}</span>
                {q.options.map((option, i) => (
                  <label key={i} className="radio-scale-label">
                    <input
                      type="radio"
                      name={`question-${index}`}
                      value={option}
                      checked={answers[index] === parseInt(option)}
                      onChange={(e) => handleChange(index, e.target.value)}
                    />
                    {option}
                  </label>
                ))}
                <span className="scale-label">{q.labels[1]}</span>
              </div>
            )}
          </div>
        ))}
        <button type="submit" className="submit-button">
          Submit
        </button>
      </form>
      {recommendation && (
        <div className="recommendation-result">
          <h3>Recommended Course:</h3>
          <p>{recommendation}</p>
        </div>
      )}
    </div>
  );
}

export default Questionnaire;