import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Logout = () => {
  const navigate = useNavigate();
  let hasLoggedOut = false; // Flag to prevent duplicate requests

  useEffect(() => {
    const token = sessionStorage.getItem('access_token');
    if (!token || hasLoggedOut) return;

    const logout = async () => {
      try {
        hasLoggedOut = true; // Set the flag to true
        const response = await axios.get('http://127.0.0.1:5000/logout', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        console.log('Logout successful:', response.data);
        sessionStorage.removeItem('access_token');
        navigate('/login');
      } catch (err) {
        console.error('Logout failed:', err);
      }
    };

    logout();
  }, [navigate]);

  return (
    <div>
      <h1>Logging out...</h1>
    </div>
  );
};

export default Logout;
