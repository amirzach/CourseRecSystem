import React from 'react';

function Recommendation({ course }) {
  return (
    <div className="container">
      <h2>Course Recommender System</h2>
      <p>The course recommended to you is:</p>
      <div className="recommendation">
        <button>{course}</button>
      </div>
    </div>
  );
}

export default Recommendation;
