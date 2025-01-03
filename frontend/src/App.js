import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router';


import './App.css';

function App() {
  function ping_api(){
    fetch('http://127.0.0.1:5000/api_test', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
      })
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
          {/* <Route path="/" element={<Game />} /> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;