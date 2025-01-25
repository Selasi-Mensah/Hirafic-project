import { useState } from "react";
import { Link } from "react-router-dom";
import logo from "../assets/download.png";

const NavBar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="flex justify-between items-center py-2 border-b border-[#161622] px-8 fixed z-50 w-full bg-[#E6E5D2]">
      <p className="text-lg font-bold">
        <img className="h-[55px] rounded-full" src={logo} />
      </p>

      <div className="hidden lg:flex gap-8 font-medium text-sm">
        <Link to="/about" className="relative group">
          Home
          <span className="absolute left-0 bottom-[-3px] h-[2px] w-0 bg-[#161622] transition-all duration-300 ease-in-out group-hover:w-full"></span>
        </Link>
        <a href="#offer" className="relative group">
          What We offer
          <span className="absolute left-0 bottom-[-3px] h-[2px] w-0 bg-[#161622] transition-all duration-300 ease-in-out group-hover:w-full"></span>
        </a>
        <a href="#meet" className="relative group">
          Meet The Team
          <span className="absolute left-0 bottom-[-3px] h-[2px] w-0 bg-[#161622] transition-all duration-300 ease-in-out group-hover:w-full"></span>
        </a>
        <Link to="/contact" className="relative group">
          Contact Us
          <span className="absolute left-0 bottom-[-3px] h-[2px] w-0 bg-[#161622] transition-all duration-300 ease-in-out group-hover:w-full"></span>
        </Link>
      </div>

      {/* Buttons */}

      {/* Hamburger Button */}
      <div className="flex items-center gap-[10px]">
        <Link
          to="/register"
          className="text-white bg-[#161622] font-medium py-1 px-6 rounded-full hidden md:block"
          onClick={() => setIsOpen(false)}
        >
          Go to Dashboard
        </Link>

        <button
          type="button"
          className="lg:hidden flex flex-col gap-1 w-8 h-8 justify-center items-center z-50 relative"
          onClick={toggleMenu}
        >
          <div
            className={`h-1 w-full bg-[#161622] transition-transform ${
              isOpen ? "rotate-45 translate-y-[6px]" : ""
            }`}
          ></div>
          <div
            className={`h-1 w-full bg-[#161622] transition-opacity ${
              isOpen ? "opacity-0" : ""
            }`}
          ></div>
          <div
            className={`h-1 w-full bg-[#161622] transition-transform ${
              isOpen ? "-rotate-45 -translate-y-[6px]" : ""
            }`}
          ></div>
        </button>
      </div>

      <div
        className={`lg:hidden fixed top-0 left-0 w-full h-full z-40 flex flex-col items-center justify-center bg-white transition-transform duration-300 ${
          isOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div
          className="absolute inset-0 bg-black opacity-25"
          onClick={() => setIsOpen(false)}
        ></div>

        <div className="relative z-50 flex flex-col items-center gap-4">
          <Link
            href="/about"
            className="text-xl font-medium py-2"
            onClick={() => setIsOpen(false)}
          >
            About
          </Link>

          <a
            href="#solution"
            className="text-xl font-medium py-2"
            onClick={() => setIsOpen(false)}
          >
            What We offer
          </a>
          <a
            href="#meet"
            className="text-xl font-medium py-2"
            onClick={() => setIsOpen(false)}
          >
            Meet The Team
          </a>
          <Link to="/contact" className="text-xl font-medium py-2">
            Contact us
          </Link>

          <Link
            to="/register"
            className="text-white bg-[#161622] font-medium text-lg py-2 px-4 rounded-full"
          >
            Join Hirafic
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NavBar;
