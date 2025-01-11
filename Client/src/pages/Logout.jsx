// filepath: /home/duaarabie/Hirafic-project/Client/src/pages/Logout.jsx
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const logout = async () => {
      try {
        const token = sessionStorage.getItem('access_token');
        await axios.get('http://127.0.0.1:5000/logout', {
          headers: {
            'Content-Type': 'application/javascript',
            Authorization: `Bearer ${token}`,
          },
        });
        sessionStorage.removeItem('access_token');
        navigate('/login');
      } catch (err) {
        console.error('Logout failed', err);
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