import OnBoard from "./components/onboard";
import ScreenOne from "./components/ScreenOne";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Client from "./pages/Client";
import Artisan from "./pages/Artisan";
import Login from "./pages/Login";
import Register from "./pages/Register";
import About from "./pages/About";

function App() {
  return (
    <>
      <Router>
        {/* <OnBoard />
        <ScreenOne /> */}
        <Routes>
          <Route path="/" element={<OnBoard />} />
          <Route path="/OnBoard" element={<ScreenOne />} />
          <Route path="/Login" element={<Login />} />
          <Route path="/Artisan" element={<Artisan />} />
          <Route path="/Client" element={<Client />} />
          <Route exact path="/home" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/About" element={<About />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
