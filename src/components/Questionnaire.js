import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles.css";

function Questionnaire({ grades, onSubmit }) {
  const [responses, setResponses] = useState({});
  const navigate = useNavigate();

  const questions = [
    {
      type: "multipleChoice",
      question: "Do you consider yourself more creative, analytical, or practical?",
      options: ["Creative", "Analytical", "Practical"],
    },
    {
      type: "multipleChoice",
      question: "Which set of skills or interests best describes you?",
      options: [
        "Problem-solving, logical thinking, and an interest in how things work. (Engineering or Technology)",
        "Curiosity about nature, scientific research, and exploring how the world works. (Science)",
        "Interest in biology, innovation, and working on solutions to health or environmental issues. (Biotechnology)",
        "Creativity in designing or making things, especially in food or other practical applications. (Food Technology or Creative Industries)",
        "Artistic talent, creativity, and a passion for visual expression. (Arts and Design)",
        "Business-minded, with an interest in finance, marketing, or entrepreneurship. (Business)",
      ],
    },
    {
      type: "multipleChoice",
      question: "How do you approach solving problems: step-by-step or intuitively?",
      options: ["Step-by-step", "Intuitively"],
    },
    {
      type: "multipleChoice",
      question: "Are you more comfortable working with data, people, or ideas?",
      options: ["Data", "People", "Ideas"],
    },
    {
      type: "radioScale",
      question: "How confident are you in your mathematical skills?",
      options: ["1", "2", "3", "4", "5"],
      labels: ["Not Confident", "Very Confident"],
    },
    {
      type: "radioScale",
      question: "How would you rate your ability to understand and apply specific scientific concepts like biology, physics and chemistry?",
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
      question: "How would you rate your artistics or visual design abilities?",
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
      question: "How would you rate your understanding of economics, accounting or business concepts?",
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
      question: "How you prefer hands-on, practical work or theoretical study?",
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

  const handleAnswerChange = (questionIndex, answer) => {
    setResponses({ ...responses, [questionIndex]: answer });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    const courseMapping = {
      Engineering: { questions: [0, 2, 14], weights: [2, 3, 1] },
      Science: { questions: [1, 9, 10], weights: [3, 2, 1] },
      Biotechnology: { questions: [1, 7, 8], weights: [3, 2, 1] },
      "Food Technology": { questions: [1, 6, 7], weights: [2, 2, 1] },
      "Fine Arts and Design": { questions: [1, 6, 16], weights: [3, 2, 1] },
      Commerce: { questions: [9, 20, 21], weights: [3, 2, 1] },
      IT: { questions: [0, 19, 14], weights: [2, 3, 1] },
      Law: { questions: [11, 3, 21], weights: [2, 2, 1] },
      Psychology: { questions: [11, 14, 20], weights: [3, 2, 1] },
      Education: { questions: [11, 23, 22], weights: [3, 2, 1] },
      "Travel and Hospitality": { questions: [21, 23, 20], weights: [3, 2, 1] },
    };
  
    const courseScores = {};
    for (const course in courseMapping) {
      courseScores[course] = 0;
    }
  
    for (const course in courseMapping) {
      const { questions, weights } = courseMapping[course];
      questions.forEach((questionIndex, idx) => {
        const response = responses[questionIndex];
        if (response) {
          const responseScore = isNaN(response) ? 1 : parseInt(response, 10);
          courseScores[course] += responseScore * weights[idx];
        }
      });
    }
  
    const maxScore = Math.max(...Object.values(courseScores));
    const normalizedScores = {};
    for (const course in courseScores) {
      normalizedScores[course] = (courseScores[course] / maxScore).toFixed(2);
    }
  
    const sortedCourses = Object.entries(normalizedScores).sort(
      (a, b) => b[1] - a[1]
    );
    const topCourse = sortedCourses[0][0];
  
    try {
      const data = {
        grades,
        responses,
        scores: normalizedScores,
      };
  
      const response = await fetch("http://localhost:5000/refine", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
  
      if (response.ok) {
        const { refinedCourse } = await response.json();
        alert(`Your recommended course is: ${refinedCourse || topCourse}`);
        navigate("/recommendation");
      } else {
        const error = await response.json();
        alert(`Failed to refine recommendation: ${error.error}`);
      }
    } catch (err) {
      console.error("Error refining recommendation:", err);
      alert("An error occurred while refining the recommendation.");
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
                      value={option}
                      checked={responses[index] === option}
                      onChange={() => handleAnswerChange(index, option)}
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
                      checked={responses[index] === option}
                      onChange={() => handleAnswerChange(index, option)}
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
    </div>
  );
}

export default Questionnaire;