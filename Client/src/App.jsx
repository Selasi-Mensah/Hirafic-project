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
        <OnBoard />
        {/* <ScreenOne /> */}
        <Routes>
          <Route path="/OnBoard" Component={<ScreenOne />} />
          <Route path="/Login" Component={<Login />} />
          <Route path="/Artisan" Component={<Artisan />} />
          <Route path="/Client" Component={<Client />} />
          <Route exact path="/Home" Component={<Home />} />
          <Route path="/register" Component={<Register />} />
          <Route path="/About" Component={<About />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
