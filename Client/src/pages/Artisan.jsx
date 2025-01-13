// import React from "react";
import Back from "../assets/Group 42.png";
import Notifications from "../assets/Not.png";
import Bookings from "../assets/Book.png";
import Profile from "../assets/Profile.png";
import pic from "../assets/me.jpeg";
import prof from "../assets/Edit-icon.png";
import { Link } from "react-router-dom";

const Artisan = () => {
  return (
    <div className="Artisan">
      <div className="header">
        <Link to="/">
          <img src={Back} alt="" />
        </Link>
        <span className="h1">Profile</span>
        <img className="img" src={prof} alt="" />
      </div>
      <div className="info">
        <div className="head">
          <img src={pic} />
          <div className="name">
            <span id="head">Paul Levites</span>
            <span id="desc">Barber</span>
          </div>
        </div>
        <div className="information">
          <div className="links">
            <div className="Link">
              <img src={Profile} alt="" />
              <Link to="/profile">Personal Information</Link>
            </div>
          </div>
          <div className="links">
            <div className="Link">
              <img src={Bookings} alt="" />
              <Link to="/book">Book Me</Link>
            </div>
          </div>
          <div className="links">
            <div className="Link">
              <img src={Notifications} alt="" />
              <Link to="/notification">Notifications</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Artisan;
/*
=======
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

export default Artisan */
