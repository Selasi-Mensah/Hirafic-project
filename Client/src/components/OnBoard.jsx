import "./component.scss";
// import ScreenOne from "./ScreenOne";
import { useNavigate } from "react-router-dom";

const onboard = () => {
  const navigate = useNavigate();

  setTimeout(() => {
    navigate("/OnBoard");
  }, 5000);
  return (
    <div className="Board">
      <span>HIRAFIC</span>
    </div>
  );
};

export default onboard;
