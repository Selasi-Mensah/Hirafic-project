// import React from "react";
import Back from "../assets/Group 42.png";
import Email from "../assets/email.png";
import user from "../assets/Profile.png";
import { Link } from "react-router-dom";

const Profile = () => {
  return (
    <div className="profile">
      <div className="header">
        <Link to="/patient">
          <img src={Back} alt="" />
        </Link>
        <span className="h1">Profile</span>
      </div>
      <div className="info">
        <span className="name">Paul Levites</span>
        <div className="information">
          <div className="details">
            <div className="name">
              <label>Full Name</label>
              <div className="texts">
                <img src={user} alt="" />
                <span>Paul Levites</span>
                <div className="border"></div>
              </div>
            </div>
            <div className="name">
              <label>Email</label>
              <div className="texts">
                <img src={Email} alt="" />
                <span>paullevites84@gmail.com</span>
                <div className="border"></div>
              </div>
            </div>
            <div className="logout">
              <span>Logout</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
