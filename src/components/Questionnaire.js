import React, { useState } from 'react';

function Questionnaire({ onNext }) {
  const [answer, setAnswer] = useState('');

  const handleAnswerChange = (newAnswer) => {
    setAnswer(newAnswer);
  };

  const handleSubmit = () => {
    onNext(answer);
  };

  return (
    <div className="container">
      <h2>Course Recommender System</h2>
      <p>You love talking about and analyzing creative works</p>
      <div className="question-buttons">
        {['Strongly Agree', 'Agree', 'Neutral', 'Disagree', 'Strongly Disagree'].map((option) => (
          <button
            key={option}
            className={answer === option ? 'selected' : ''}
            onClick={() => handleAnswerChange(option)}
          >
            {option}
          </button>
        ))}
      </div>
      <div className="arrow-buttons">
        <button onClick={() => onNext('back')}>⟵</button>
        <button onClick={handleSubmit}>⟶</button>
      </div>
    </div>
  );
}

export default Questionnaire;
