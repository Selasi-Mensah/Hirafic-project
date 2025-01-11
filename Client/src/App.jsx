import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import RegistrationForm from './pages/Register';
import Login from './pages/Login';
import Artisan from './pages/Artisan';
import Client from './pages/Client';
import Logout from './pages/Logout';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<RegistrationForm />} />
        <Route path="/login" element={<Login />} />
        <Route path="/artisan" element={<Artisan />} />
        <Route path="/artisan/:usename" element={<Artisan />} />
        <Route path="/client" element={<Client />} />
        <Route path="/client/:username" element={<Client />} />
        <Route path="/logout" element={<Logout />} />
      </Routes>
    </Router>
  )
}


export default App;
