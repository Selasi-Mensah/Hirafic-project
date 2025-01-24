import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Logout = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);

  let hasLoggedOut = false; // Flag to prevent duplicate requests

  useEffect(() => {
    const token = sessionStorage.getItem('access_token');
    if (!token || hasLoggedOut) {
      navigate('/login',  { replace: true });
      return;
    }

    const logout = async () => {
      try {
        // console.log(token)
        hasLoggedOut = true; // Set the flag to true
        const response = await axios.get('http://127.0.0.1:5000/logout', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        sessionStorage.removeItem('access_token');
        sessionStorage.clear();
        navigate('/login',  { replace: true });
        console.log('Logout successful:', response.data);
      } catch (err) {
        sessionStorage.removeItem('access_token');
        sessionStorage.clear();
        console.error('Logout failed:', err);
        if (err.response && err.response.status === 401) {
          console.log('token expired, redirecting to login');
        }
      } finally {
        // sessionStorage.removeItem('access_token');
        // sessionStorage.clear();
        // navigate('/login',  { replace: true });
        setLoading(false);
      }
    };

    logout();
  }, [navigate]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Logging out...</h1>
    </div>
  );
};

export default Logout;
