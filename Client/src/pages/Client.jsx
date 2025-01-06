import Back from "../assets/Group 42.png";
// import Notifications from "../assets/Not.png";
import Bookings from "../assets/Book.png";
import Profile from "../assets/Profile.png";
import pic from "../assets/me.jpeg";
import prof from "../assets/Edit-icon.png";
import { Link } from "react-router-dom";
const Client = () => {
  return (
    <div className="client">
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
              <img src={Profile} alt="" />
              <Link to="/profile">Personal Information</Link>
            </div>
          </div>
          <div className="links">
            <div className="Link">
              <img src={Bookings} alt="" />
              <Link to="/search">Search Artisans</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Client;
