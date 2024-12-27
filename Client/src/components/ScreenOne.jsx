import description from "../assets/Group 1.png";
// import { Link } from "react-router-dom";
import { Link } from "react-router-dom";

const ScreenOne = () => {
  return (
    <div className="screen">
      <div className="img">
        <img src={description} alt="" />
      </div>
      <div className="texts">
        <span>Freelancing Platform for Atisans</span>
        <small>
          Connect with clients all over the world, and get paid for your skills.
        </small>
      </div>
        <Link className="btn" id="link" to="/register">Join Us Now</Link>
    </div>
  );
};

export default ScreenOne;
