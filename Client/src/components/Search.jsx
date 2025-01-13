// import React from 'react'
import { Link } from "react-router-dom";
import Back from "../assets/Group 42.png";
const Search = () => {
  return (
    <div className="search">
      <div className="header">
        <Link to="/profile">
          <img src={Back} alt="" />
        </Link>
        <span className="h1">Search</span>
        {/* <img className="img" src={prof} alt="" /> */}
      </div>
      <div className="input">
        <input type="search" placeholder="Search Artisan" />
        <div className="btn">submit</div>
      </div>
    </div>
  );
};

export default Search;
