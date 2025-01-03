// src/components/About.js
import React from 'react';
import './About.css'; // Link to the About.css file

const About = () => {
  return (
    <div className="about-section">
      <h3>About Us</h3>
      <p className='about-text'>
        Welcome to our innovative application, designed to seamlessly bridge the gap between user-friendly interfaces and cutting-edge technology. This platform empowers users to upload Excel (.xlsx) files and harness the power of natural language to achieve their goals.
        Our unique system allows users to input queries in their own words, simplifying complex data interactions. Leveraging advanced Large Language Models (LLM), the application interprets these natural language queries and generates precise, actionable output queries tailored to the user's requirements.      
      </p>
      <p className='about-text'>
        With a focus on productivity and efficiency, this application is perfect for professionals and businesses seeking a streamlined approach to data analysis and query generation. Whether you're an expert or a novice, our solution ensures that data-driven decision-making is more accessible and intuitive than ever before.
        Discover a smarter way to work with data. Welcome to the future of query generation!
      </p>


      <div className="image-section">
        <div className="image-container">
          <img
            src="https://vector.cloobot.ai/backend/database_download?file_id=d4d9cf5a-5dea-4192-a212-f693e027d15f"
            alt="SQL Query Illustration"
            className="about-image"
          />
          <p className="image-caption">Illustration of SQL Query Generation</p>
        </div>
        <div className="image-container">
          <img
            src="https://vector.cloobot.ai/backend/database_download?file_id=31205a30-5ab6-4478-bb13-9a8517b31547" // Replace with your actual XLSX image URL
            alt="XLSX File Illustration"
            className="about-image-xlsx"
          />
          <p className="image-caption">Illustration of XLSX File Interaction</p>
        </div>
      </div>
    </div>
  );
};

export default About;
