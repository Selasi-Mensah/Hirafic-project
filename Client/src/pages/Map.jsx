import { useState, useEffect } from "react";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Slider from "@mui/material/Slider";
import Button from "@mui/material/Button";
import SearchIcon from "@mui/icons-material/Search";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import { MapContainer, Marker, Popup, TileLayer, useMap } from "react-leaflet";
import axios from "axios";

// Component to dynamically center the map based on coordinates
const LocationPointer = ({ position }) => {
  const map = useMap();
  useEffect(() => {
    if (position) {
      map.setView(position, 13); // Set map view to user's position with zoom 13
    }
  }, [position, map]);
  return position ? (
    <Marker position={position}>
      <Popup>
        <strong>Your Location</strong>
      </Popup>
    </Marker>
  ) : null;
};

const Map = () => {
  const [distance, setDistance] = useState(5000); // Search radius
  const [artisans, setArtisans] = useState([]); // List of artisans
  const [searchQuery, setSearchQuery] = useState(""); // User's search input
  const [mapCenter, setMapCenter] = useState([6.5244, 3.3792]); // Default to Lagos, Nigeria
  const [userLocation, setUserLocation] = useState(null); // User's current location

  // Fetch user's current location
  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        setUserLocation([latitude, longitude]);
        setMapCenter([latitude, longitude]); // Center map to user's location
      },
      (error) => {
        console.error("Error getting location:", error);
        alert("Unable to fetch your location. Using default center.");
      }
    );
  }, []);

  // Fetch artisans from the backend with the token
  const fetchArtisans = async () => {
    try {
      const token = sessionStorage.getItem("access_token"); // Retrieve the token from sessionStorage
      if (!token) {
        alert("You are not authenticated. Please log in.");
        return;
      }

      const response = await axios.post(
        "http://127.0.0.1:5000/artisan",
        {
          query: searchQuery,
          distance: distance,
        },
        {
          headers: {
            "Content-Type": "application/json", // Correct content type
            Authorization: `Bearer ${token}`, // Attach token to the Authorization header
          },
        }
      );

      setArtisans(response.data);

      if (response.data.length > 0) {
        setMapCenter([response.data[0].latitude, response.data[0].longitude]);
      } else {
        alert("No artisans found nearby.");
      }
    } catch (error) {
      console.error("Error fetching artisans:", error);
      alert("Unable to fetch artisans. Please try again later.");
    }
  };

  // Reset the search form and map
  const resetSearch = () => {
    setSearchQuery("");
    setDistance(5000);
    setArtisans([]);
    setMapCenter(userLocation || [6.5244, 3.3792]); // Reset to user location
  };

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
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Typography>Distance:</Typography>
          <Slider
            style={{ width: "75%" }}
            value={distance}
            onChange={(e, newValue) => setDistance(newValue)}
            min={1000}
            max={20000}
            step={500}
          />
        </div>
        <div>
          <Button style={{ width: "50%" }} variant="outlined" onClick={resetSearch}>
            <RestartAltIcon />
            Reset
          </Button>
          <Button style={{ width: "50%" }} variant="contained" onClick={fetchArtisans}>
            <SearchIcon />
            Search
          </Button>
        </div>
      </div>
      <div>
        <MapContainer
          center={mapCenter}
          zoom={13}
          scrollWheelZoom={false}
          style={{ height: "400px", marginTop: "1rem" }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {/* Location Pointer */}
          <LocationPointer position={userLocation} />
          {/* Artisans Markers */}
          {artisans.map((artisan, index) => (
            <Marker key={index} position={[artisan.latitude, artisan.longitude]}>
              <Popup>
                <strong>{artisan.name}</strong>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
};

export default Map;
