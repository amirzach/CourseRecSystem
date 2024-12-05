import React, { useState } from 'react';
import "../styles.css";

function GradeSelection({ onNext }) {
  const [grades, setGrades] = useState({
    bahasaMalaysia: '',
    sejarah: '',
    english: '',
    maths: '',
    pendidikanIslam: '',
    pendidikanMoral: ''
  });

  const [newSubject, setNewSubject] = useState('');

  const handleGradeChange = (e) => {
    setGrades({ ...grades, [e.target.name]: e.target.value });
  };

  const handleAddSubject = () => {
    if (newSubject.trim() && !grades[newSubject]) {
      setGrades({ ...grades, [newSubject]: '' });
      setNewSubject('');
    }
  };

  const handleSubmit = () => {
    onNext(grades);
  };

  return (
    <div className="container">
      <h2>Course Recommender System</h2>
      <p>Enter your grade for each subject</p>

      <div className="subject-list">
        {Object.keys(grades).map((subject) => (
          <div key={subject} className="subject-item">
            <label className="subject-label">
              {subject.replace(/([A-Z])/g, ' $1').toLowerCase()}
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
              <option value="A-">A-</option>'A+': 4.3, 'A': 4, 'A-': 3.7, 'B+': 3.3, 'B': 3, 'B-': 2.7, 'C': 2, 'D': 1, 'E': 0.5, 'F': 0}
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

      <button onClick={handleSubmit} className="submit-button">
        Next
      </button>
    </div>
  );
}

export default GradeSelection;
