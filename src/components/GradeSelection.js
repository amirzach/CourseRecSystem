import React, { useState } from 'react';

function GradeSelection({ onNext }) {
  const [grades, setGrades] = useState({
    bahasaMalaysia: '',
    sejarah: '',
    english: '',
    maths: '',
    pendidikanIslam: '',
    pendidikanMoral: ''
  });

  const handleGradeChange = (e) => {
    setGrades({ ...grades, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    onNext(grades);
  };

  return (
    <div className="container">
      <h2>Course Recommender System</h2>
      <p>Enter your grade for each subject</p>
      {Object.keys(grades).map((subject) => (
        <div key={subject}>
          <label>{subject.replace(/([A-Z])/g, ' $1')}</label>
          <select name={subject} value={grades[subject]} onChange={handleGradeChange}>
            <option value="">Select</option>
            <option value="A+">A+</option>
            <option value="A">A</option>
            <option value="A-">A-</option>
          </select>
        </div>
      ))}
      <button onClick={handleSubmit}>Next</button>
    </div>
  );
}

export default GradeSelection;
