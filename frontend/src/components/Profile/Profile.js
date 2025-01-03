// src/components/Profile.js
import React, { useState, useEffect } from 'react';
import './Profile.css'; // Link to the Profile.css file
import httpClient from '../../httpClient'; // Import your HTTP client

const Profile = () => {
  const [userDetails, setUserDetails] = useState({ username: '', email: '' });
  const [error, setError] = useState('');

  // Fetch user details when the component mounts
  useEffect(() => {
    const fetchUserDetails = async () => {
      const user_id = localStorage.getItem('user_id'); // Get user ID from local storage
      try {
        const response = await httpClient.get('/getUserDetails',user_id); // Replace with your API endpoint
        setUserDetails({
          username: response.data.username,
          email: response.data.email,
        });
      } catch (err) {
        setError('Failed to fetch user details. Please try again later.');
        console.error('Error fetching user details:', err);
      }
    };

    fetchUserDetails();
  }, []); // Empty dependency array ensures this runs only once when the component mounts

  return (
    <div className="profile-section">
      <h3>Your Profile</h3>
      {error ? (
        <p className="error-message">{error}</p>
      ) : (
        <div className="profile-details">
          <p>
            <strong>Username:</strong> {userDetails.username}
          </p>
          <p>
            <strong>Email:</strong> {userDetails.email}
          </p>
        </div>
      )}
    </div>
  );
};

export default Profile;
