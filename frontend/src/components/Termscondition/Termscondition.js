// src/components/TermsConditions.js
import React from 'react';
import './Termscondition.css'; // Link to the Termscondition.css file

const TermsConditions = () => {
  return (
    <div className="terms-conditions-section">
      <h3>Terms and Conditions</h3>
      <p className="term-text">Effective Date: 04 January 2025</p>
      <p className="term-text">
        Welcome to our application. By accessing or using this application, you agree to comply with the following terms and conditions. Please read them carefully before proceeding.
      </p>
      <div className="term-text">
        <strong>1. Acceptance of Terms</strong>
        <p>
          By using this application, you acknowledge that you have read, understood, and agree to be bound by these terms and conditions. If you do not agree, please refrain from using the application.
        </p>
      </div>
      <div className="term-text">
        <strong>2. User Responsibilities</strong>
        <p>Users must provide accurate and complete information when registering or uploading files.</p>
        <p>Uploaded files must be in .xlsx format and comply with all applicable laws and regulations.</p>
        <p>Users are solely responsible for the content of the files they upload and any queries they submit.</p>
      </div>
      <div className="term-text">
        <strong>3. Permitted Use</strong>
        <p>
          This application is intended for personal or professional use to generate queries based on user-provided input. Any misuse, including but not limited to unauthorized access, reverse engineering, or interfering with the application’s operations, is strictly prohibited.
        </p>
      </div>
      <div className="term-text">
        <strong>4. Data Privacy and Security</strong>
        <p>
          Uploaded files and query inputs are processed securely and in accordance with our Privacy Policy.
        </p>
        <p>
          We take reasonable measures to protect user data but cannot guarantee absolute security. Users are encouraged to avoid uploading sensitive or confidential information.
        </p>
      </div>
      <div className="term-text">
        <strong>5. LLM Module and Query Outputs</strong>
        <p>
          The application leverages advanced Large Language Models (LLM) to generate query outputs based on user inputs.
        </p>
        <p>
          While every effort is made to provide accurate outputs, the application does not guarantee the accuracy, completeness, or reliability of results.
        </p>
        <p>
          Users are advised to verify outputs independently before using them for critical purposes.
        </p>
      </div>
      <div className="term-text">
        <strong>6. Intellectual Property</strong>
        <p>
          The application and its components, including but not limited to software, design, and content, are the intellectual property of the developers and are protected by applicable laws.
        </p>
        <p>
          Users retain ownership of their uploaded files but grant the application a limited license to process them for query generation purposes.
        </p>
      </div>
      <div className="term-text">
        <strong>7. Limitation of Liability</strong>
        <p>
          The application is provided "as is" without any warranties, express or implied.
        </p>
        <p>
          We are not liable for any direct, indirect, incidental, or consequential damages arising from the use or inability to use the application.
        </p>
      </div>
      <div className="term-text">
        <strong>8. Termination</strong>
        <p>
          We reserve the right to suspend or terminate user access to the application at our discretion, including but not limited to violations of these terms.
        </p>
      </div>
      <div className="term-text">
        <strong>9. Modifications</strong>
        <p>
          We may update these terms and conditions from time to time. Continued use of the application after changes are made constitutes acceptance of the revised terms.
        </p>
      </div>
      <div className="term-text">
        <strong>10. Governing Law</strong>
        <p>
          These terms shall be governed by and construed in accordance with the laws of [Insert Jurisdiction].
        </p>
      </div>
      <div className="term-text">
        <strong>Contact Us</strong>
        <p>
          If you have any questions or concerns regarding these terms, please contact us at [Insert Contact Information].
        </p>
      </div>
    </div>
  );
};

export default TermsConditions;
