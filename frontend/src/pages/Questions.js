import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ArrowRight, Home } from 'lucide-react';
import axios from 'axios';

const Questions = () => {
  const location = useLocation();
  const navigate = useNavigate(); // Use navigate for redirection
  const { selectedCourse } = location.state;
  const [topic, setTopic] = useState('');
  const [questions, setQuestions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [feedback, setFeedback] = useState(null);
  const [showResults, setShowResults] = useState(false);
  const [hasAnswered, setHasAnswered] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError(null);

    try {
      const data = {
        subject: selectedCourse.name.toLowerCase().replace(/\s/g, '_'),
        storage_path: `${selectedCourse.name.toLowerCase().replace(/\s/g, '_')}_db`,
        query: topic
      };

      const response = await axios.post('http://127.0.0.1:5000/ai/practice_questions', data);
      setQuestions(response.data);
      setCurrentQuestionIndex(0);
      setScore(0);
      setShowResults(false);
      setFeedback(null);
      setHasAnswered(false);
      setTopic('')
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to fetch questions');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerClick = (choiceIndex) => {
    if (!questions || !questions.questions[currentQuestionIndex]) return;

    const correctIndex = questions.correct_answers[currentQuestionIndex];
    if (choiceIndex === correctIndex) {
      setScore(score + 1);
      setFeedback({ isCorrect: true, message: 'Correct!' });
    } else {
      setFeedback({ isCorrect: false, message: 'Wrong! Try again.' });
    }
    setHasAnswered(true);
  };

  const handleNextQuestion = () => {
    if (!questions || currentQuestionIndex >= questions.questions.length - 1) {
      setShowResults(true);
      return;
    }

    setCurrentQuestionIndex(currentQuestionIndex + 1);
    setFeedback(null);
    setHasAnswered(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen  p-4">
      {/* Home Button */}
      <button
        onClick={() => navigate('/home')}
        className="absolute top-4 left-4 bg-gray-200 p-2 rounded-full shadow-md hover:bg-gray-300 transition-colors"
      >
        <Home size={24} />
      </button>

      <h1 className="text-4xl font-bold text-gray-800 mb-4">{selectedCourse.name}</h1>

      {/* Input form for topic */}
      <form onSubmit={handleSubmit} className="w-full max-w-2xl mb-8">
        <div className="flex gap-2">
          <input
            id="topic"
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="What topics would you like to practice?"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-[#9E72C3] focus:border-[#9E72C3]"
            disabled={loading}
          />
          <button
            type="submit"
            className="bg-[#9E72C3] text-white px-4 py-2 rounded-md hover:bg-purple-700 transition-colors duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={loading || !topic.trim()}
          >
            <span>{loading ? 'Loading...' : 'Submit'}</span>
            {!loading && <ArrowRight size={20} />}
          </button>
        </div>
      </form>

      {error && (
        <div className="w-full max-w-2xl p-4 mb-4 bg-red-100 text-red-700 rounded-md">
          {error}
        </div>
      )}

      {/* Render questions only if they exist */}
      {questions && !showResults && (
        <div className="w-full max-w-2xl bg-[#9E72C3] text-white p-6 rounded-md shadow-md">
          <div className="flex justify-between mb-4">
            <span className="text-lg">Score: {score}/{questions.questions.length}</span>
            <span className="text-lg">Question {currentQuestionIndex + 1}/{questions.questions.length}</span>
          </div>

          <h2 className="text-2xl font-semibold mb-6">{questions.questions[currentQuestionIndex][0]}</h2>

          <div className="grid grid-cols-2 gap-4">
            {questions.questions[currentQuestionIndex].slice(1).map((choice, index) => (
              <button
                key={index}
                onClick={() => handleAnswerClick(index)}
                className="bg-white text-gray-800 p-4 rounded-md hover:bg-gray-200 transition-colors"
                disabled={hasAnswered}
              >
                {choice}
              </button>
            ))}
          </div>

          {feedback && (
            <div
              className={`mt-6 p-4 rounded-md text-center ${
                feedback.isCorrect ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              }`}
            >
              {feedback.message}
            </div>
          )}

          {hasAnswered && (
            <button
              onClick={handleNextQuestion}
              className="mt-6 bg-white text-gray-800 px-4 py-2 rounded-md hover:bg-gray-200 transition-colors"
            >
              {currentQuestionIndex < questions.questions.length - 1 ? 'Next Question' : 'View Results'}
            </button>
          )}
        </div>
      )}

      {showResults && (
        <div className="w-full max-w-2xl bg-white text-gray-800 p-6 rounded-md shadow-md">
          <h2 className="text-3xl font-semibold mb-4">Quiz Results</h2>
          <p className="text-lg">You scored {score} out of {questions.questions.length}!</p>
          <p className="text-lg">{score >= 7 ? 'Great job!' : 'Keep practicing!'}</p>
        </div>
      )}
    </div>
  );
};

export default Questions;
