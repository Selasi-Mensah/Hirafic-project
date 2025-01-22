import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import OnBoard from "./components/OnBoard";
import ScreenOne from "./components/ScreenOne";
import Home from "./pages/Home";
import Client from "./pages/Client";
import Artisan from "./pages/Artisan";
import Login from "./pages/Login";
import Register from "./pages/Register";
import About from "./pages/About";
import Logout from "./pages/Logout";
import "./app.scss";
import Search from "./components/Search";
import Map from "./pages/Map";
// import Profile from "./components/Profile";

function App() {
  return (
    <>
      <Router>
        {/* <OnBoard />
        <ScreenOne /> */}
        <Routes>
          <Route path="/" element={<OnBoard />} />
          <Route path="/OnBoard" element={<ScreenOne />} />
          <Route path="/login" element={<Login />} />
          <Route path="/artisan" element={<Artisan />} />
          <Route path="/artisan/:username" element={<Artisan />} />
          <Route path="/client" element={<Client />} />
          <Route path="/client/:username" element={<Client />} />
          <Route exact path="/home" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/about" element={<About />} />
          <Route path="/search" element={<Search />} />
          {/* <Route path="/profile" element={<Profile />} /> */}
          <Route path="/map/:mapId" element={<Map />} />
          <Route path="/logout" element={<Logout />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
