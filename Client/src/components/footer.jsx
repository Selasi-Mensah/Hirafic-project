import { useEffect, useState } from "react";
// import firstAid from "./../assets/first-aid.svg";
// import health from "./../assets/health-healthcare.svg";
import { Link } from "react-router-dom";
// import logo from "../assets/download.png";

const Footer = () => {
  const [year, setYear] = useState(new Date().getFullYear());

  useEffect(() => {
    setYear(new Date().getFullYear());
  }, []);
  return (
    <div
      id="footer"
      className="text-white bg-[#202020] pt-[50px] md:pt-[90px] px-[30px]"
    >
      <div className="text-center">
        <p className="font-semibold text-[20px] md:text-[30px] leading-[28px] md:leading-[80px] pb-[20px]">
        Hirafic: Empowering Artisans, Connecting Communities
        </p>
        <span className="flex flex-col justify-center items-center gap-[20px] py-[30px]">
          {/* <img src={health} alt="" height={40} width={40} /> */}

          <span className="flex gap-[20px]">
            <Link
              to="/Register"
              className="py-[10px] px-[30px] md:px-[40px] text-[14px] md:text-[16px] rounded-[8px] bg-blue-500 text-white font-medium"
            >
              Get Started
            </Link>
            {/* <Link
              to="/contact"
              className="py-[20px] px-[20px] md:px-[40px] text-[14px] md:text-[16px] rounded-[8px] bg-green-500 text-white font-medium"
            >
              Contact Us
            </Link> */}
          </span>
        </span>
      </div>

      <div className="flex /px-[30px] justify-between my-[40px] flex-col md:flex-row gap-[20px] md:gap-[0px]">
        {/* <div>
          <img className="h-[35px] rounded-full" src={logo} alt="" />
          <p className="text-[18px] font-semibold leading-[24px]">
            Hirafic: Empowering Artisans, Connecting Communities
          </p>
        </div> */}

        <div className="flex flex-col gap-[14px] footer-links">
          <p className="font-semibold text-[18px] leading-[24px] text-blue-500">
            Get to know us
          </p>
          <Link to="/about" className="text-[14px] leading-[20px]">
            Home
          </Link>
          <a href="#meet" className="text-[14px] leading-[20px]">
            Meet The Team
          </a>
        </div>

        <div className="flex flex-col gap-[14px] footer-links">
          <p className="font-semibold text-[18px] leading-[24px] text-blue-500">
            Our Services
          </p>
          <Link href="/register" className="text-[14px] leading-[20px]">
            Join Hirafic
          </Link>
          <Link to="/contact" className="text-[14px] leading-[20px]">
            Contact Us
          </Link>
        </div>
      </div>

      <p className="border-t-[1px] border-white /mt-[20px] text-[#F5FFFBCC] py-[20px]  text-center font-[400] text-[16px] md:text-[18px] leading-[28px]">
        © {year} Hirafic Team · All rights reserved.
      </p>
    </div>
  );
};

export default Footer;
