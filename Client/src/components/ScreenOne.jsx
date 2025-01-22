import description from "../assets/Group 1.png";
// import { Link } from "react-router-dom";
import { Link } from "react-router-dom";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const ScreenOne = () => {

  const navigate = useNavigate();
  useEffect(() => {
    // if user is already logged in, redirect to their dashboard
    if (sessionStorage.getItem('access_token')) {
      const username = sessionStorage.getItem('username');
      if (sessionStorage.getItem('role') === 'Artisan') {
        navigate(`/artisan/${username}`);
        // window.location.href = `/artisan/${username}`;
      }
      else {
        navigate(`/client/${username}`);
        // window.location.href = `/client/${username}`;
      }
    }
  }, [navigate]);

  return (
    <div className="screen">
      <div className="img">
        <img src={description} alt="" />
      </div>
      <div className="texts">
        <span>Freelancing Platform for Artisans</span>
        <small>
          Connect with clients all over the world, and get paid for your skills.
        </small>
      </div>
        <Link className="btn" id="link" to="/register">Join Us Now</Link>
    </div>
  );
};

export default ScreenOne;
