import React, { useState } from 'react';
import GradeSelection from './components/GradeSelection';
import Questionnaire from './components/Questionnaire';
import Recommendation from './components/Recommendation';
import './styles.css';

function App() {
  const [step, setStep] = useState(1);
  const [grades, setGrades] = useState({});
  const [answer, setAnswer] = useState('');
  const [course, setCourse] = useState('');

  const handleGradeSubmit = (submittedGrades) => {
    setGrades(submittedGrades);
    setStep(2);
  };

  const handleAnswerSubmit = (submittedAnswer) => {
    if (submittedAnswer === 'back') {
      setStep(1);
      return;
    }
    setAnswer(submittedAnswer);
    const recommendedCourse = submittedAnswer.includes('Agree') ? 'Computer Science' : 'Literature';
    setCourse(recommendedCourse);
    setStep(3);
  };

  return (
    <div className="app">
      {step === 1 && <GradeSelection onNext={handleGradeSubmit} />}
      {step === 2 && <Questionnaire onNext={handleAnswerSubmit} />}
      {step === 3 && <Recommendation course={course} />}
    </div>
  );
}

export default App;
