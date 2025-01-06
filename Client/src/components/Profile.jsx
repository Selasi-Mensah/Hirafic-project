// import React from 'react'
import Back from "../assets/Group 42.png";
// import Email from "../assets/email.png";
// import user from "../assets/Profile.png";
import { Link } from "react-router-dom";
import pic from "../assets/me.jpeg";
import prof from "../assets/Edit-icon.png";

const Profile = () => {
  return (
    <div className="profile">
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
          </div>
        </div>
        <div className="information">
          <div className="links">
            <div className="Link">
              {/* <img src={Email} alt="" /> */}
              <label>Email</label>
              <a href="mailto:paullevites84@gmail.com">
                Paullevites84@gmail.com
              </a>
            </div>
          </div>
          <div className="links">
            <div className="Link">
              {/* <img src={user} alt="" /> */}
              <label>Adrress</label>
              <span>Dummy adrress</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
