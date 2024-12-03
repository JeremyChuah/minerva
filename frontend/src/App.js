import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import Questions from './pages/Questions';

function App() {
  return (
    <Router>
      <div>

        {/* Define Routes */}
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/home" element={<Home />} />
          <Route path="/practice-questions" element={<Questions />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
