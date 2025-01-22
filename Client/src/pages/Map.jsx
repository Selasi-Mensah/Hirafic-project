// import React from "react";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Slider from "@mui/material/Slider";
import Button from "@mui/material/Button";
import SearchIcon from "@mui/icons-material/Search";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import { MapContainer, Marker, Popup, TileLayer, useMap } from "react-leaflet";
// import GoogleMapReact from "google-map-react";

const Map = () => {
  //   header = () => {
  //     return (

  //     );
  //   };
  //   map = () => {

  //   };
  return (
    <div style={{ backgroundColor: "beige", margin: ".5rem" }}>
      <div>
        <Typography variant="h4" style={{ textAlign: "center" }}>
          Search Artisan
        </Typography>
        <TextField
          style={{ width: "100%" }}
          variant="outlined"
          label="Search for Artisan"
        ></TextField>
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Typography>Distance:</Typography>
          <Slider style={{ width: "75%" }} />
        </div>
        <div>
          <Button style={{ width: "50%" }} variant="outlined">
            <RestartAltIcon />
            Reset
          </Button>
          <Button style={{ width: "50%" }} variant="contained">
            <SearchIcon />
            Search
          </Button>
        </div>
      </div>
      return
      <div>
        <MapContainer
          center={[51.505, -0.09]}
          zoom={13}
          scrollWheelZoom={false}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <Marker position={[51.505, -0.09]}>
            <Popup>This is a popup</Popup>
          </Marker>
        </MapContainer>
      </div>
      ;
      {/* {this.header()}
      {this.map()} */}
    </div>
  );
};

export default Map;
