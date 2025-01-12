import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Artisan = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const accessProtected = async () => {
    try {
      if (!token) throw new Error('No token available');
      const response = await axios.get('http://127.0.0.1:5000/protected', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setProtectedData(response.data);
    } catch (err) {
      setError(err.response ? err.response.data : err.message);
    }
  };
  useEffect(() => {
    const fetchData = async () => {
      try {
        let token = sessionStorage.getItem('access_token');
        /// console.log(token);
        if (!token || typeof token !== 'string') {
          throw new Error('No access token found or token is not a string');
        }
        const response = await axios.get('http://127.0.0.1:5000/artisan', {
          headers: {
            'Content-Type': 'application/javascript',
            'Authorization': `Bearer ${token}`,

          },
        });
        setData(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>Artisan Data</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );

};

export default Artisan;

