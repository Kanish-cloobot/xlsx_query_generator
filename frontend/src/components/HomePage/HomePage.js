import React from "react";
import { Link, Outlet } from "react-router-dom"; // Import Link and Outlet for routing
import "./HomePage.css";
import About from "../About/About";
import Profile from "../Profile/Profile";
import TermsConditions from "../Termscondition/Termscondition";

const HomePage = () => {
  return (
    <section className="home-container">
      <div className="colour"></div>
      <div className="colour"></div>
      <div className="colour"></div>

      <div className="layout">
        {/* Floating Navigation Bar */}
        <div className="navbar">
        <h3 className="nav-head">SQL Query Generator</h3>
          <div className="nav-items">
            
            <Link to="about" className="nav-item">
              About
            </Link>
            <Link to="profile" className="nav-item">
              Profile
            </Link>
            <Link to="action" className="nav-item">
              Action
            </Link>
            <Link to="terms-conditions" className="nav-item">
              Terms and Conditions
            </Link>
            <Link to="/" className="nav-item">
              Logout
            </Link>
            
          </div>
        </div>

        {/* Dynamic Content Area */}
        <div className="content-area">
          {/* This will render the matched route component */}
          <Outlet />
        </div>
      </div>
    </section>
  );
};

export default HomePage;
