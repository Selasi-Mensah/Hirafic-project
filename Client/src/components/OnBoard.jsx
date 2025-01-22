import "./component.scss";
// import ScreenOne from "./ScreenOne";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

const OnBoard = () => {
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
    } else {
      setTimeout(() => {
        navigate("/OnBoard");
      }, 5000);
    }
  }, [navigate]);

  return (
    <div className="Board">
      <span>HIRAFIC</span>
    </div>
  );
};

export default OnBoard;
