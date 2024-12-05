import React, { useState } from "react";
import "../styles.css";

function Questionnaire({ onSubmit }) {
  const [responses, setResponses] = useState({});

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
  ];

  const handleAnswerChange = (questionIndex, answer) => {
    setResponses({ ...responses, [questionIndex]: answer });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(responses);
  };

  return (
    <div className="container">
      <h2>Course Recommender System</h2>
      <form onSubmit={handleSubmit}>
        {questions.map((q, index) => (
          <div key={index} className="question">
            <p>{q.question}</p>
            {q.type === "multipleChoice" ? (
              <div className="horizontal-options">
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
