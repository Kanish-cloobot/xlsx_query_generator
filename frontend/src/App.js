import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AuthPage from './components/AuthPage/AuthPage';
import HomePage from './components/HomePage/HomePage';
import About from './components/About/About';
import Profile from './components/Profile/Profile';
import TermsConditions from './components/Termscondition/Termscondition';
import Actions from './components/Actions/Actions';

import './App.css';

function App() {
  function ping_api() {
    fetch('http://127.0.0.1:5000/api_test', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<AuthPage />} />
          <Route path="/home" element={<HomePage />}>
            <Route path="about" element={<About />} />
            <Route path="profile" element={<Profile />} />
            <Route path="terms-conditions" element={<TermsConditions />} />
            <Route path="action" element={<Actions />} />
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
