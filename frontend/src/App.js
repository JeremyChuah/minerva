import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import Questions from './pages/Questions';
import LandingPage from './pages/LandingPage';
import Chatbot from './pages/Chatbot';
import Review from './pages/Review';

function App() {
  return (
    <Router>
      <div>

        {/* Define Routes */}
        <Routes>
          <Route path="/" element={<LandingPage/>}/>
          <Route path="/home" element={<Home />} />
          <Route path="/practice-questions" element={<Questions />} />
          <Route path="/review" element={<Review />} />
          <Route path="/chatbot" element={<Chatbot />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
