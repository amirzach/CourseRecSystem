import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import GradeSelection from "./components/GradeSelection";
import Questionnaire from "./components/Questionnaire";
import Recommendation from "./components/Recommendation";
import "./styles.css";

function App() {
  const [grades, setGrades] = useState({});
  const [responses, setResponses] = useState({});

  return (
    <Router>
      <div className="app">
        <Routes>
          <Route
            path="/"
            element={<GradeSelection onNext={(submittedGrades) => setGrades(submittedGrades)} />}
          />
          <Route
            path="/questionnaire"
            element={<Questionnaire grades={grades} onSubmit={(submittedResponses) => setResponses(submittedResponses)} />}
          />
          <Route
            path="/recommendation"
            element={<Recommendation responses={responses} />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
