// src/HomePage.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css'; // Import the same or new styles for the home page
import About from '../About/About';
import HowToUse from '../About/About';
import Profile from '../Profile/Profile';
import TermsConditions from '../Termscondition/Termscondition';

const HomePage = () => {
  const [selectedSection, setSelectedSection] = useState("About");

  const handleNavigationClick = (section) => {
    setSelectedSection(section);
  };

  const renderSection = () => {
    switch (selectedSection) {
      case "About":
        return <About />;
      case "HowToUse":
        return <HowToUse />;
      case "Profile":
        return <Profile />;
      case "TermsConditions":
        return <TermsConditions />;
      default:
        return <About />;
    }
  };

  return (
    <section className="home-container">
      <div className="colour"></div>
      <div className="colour"></div>
      <div className="colour"></div>

      <div className="layout">
        {/* Floating Navigation Bar */}
        <div className="navbar">
          <h2>Navigation</h2>
          <div className="nav-items">
            <Link to="#" onClick={() => handleNavigationClick("About")} className="nav-item">
              About
            </Link>
            <Link to="#" onClick={() => handleNavigationClick("HowToUse")} className="nav-item">
              How to Use
            </Link>
            <Link to="#" onClick={() => handleNavigationClick("Profile")} className="nav-item">
              Profile
            </Link>
            <Link to="#" onClick={() => handleNavigationClick("TermsConditions")} className="nav-item">
              Terms and Conditions
            </Link>
          </div>
        </div>

        {/* Dynamic Content Area */}
        <div className="content-area">
          {renderSection()}
        </div>
      </div>
    </section>
  );
};

export default HomePage;
