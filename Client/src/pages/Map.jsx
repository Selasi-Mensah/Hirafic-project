import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Slider from "@mui/material/Slider";
import Button from "@mui/material/Button";
import Modal from "@mui/material/Modal";
import Box from "@mui/material/Box";
import SearchIcon from "@mui/icons-material/Search";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import { useState, useEffect } from "react";
import ArtisanInfo from "@/components/ArtisanInfo";

const Map = () => {
  const [artisans, setArtisans] = useState([]);
  const token = sessionStorage.getItem("access_token");
  const [loading, setLoading] = useState(false);
  const [distance, setDistance] = useState();
  const [selectedArtisan, setSelectedArtisan] = useState(null);

  const fetchArtisans = async () => {
    try {
      setLoading(true);
      const endpoint = distance ? `/nearby_artisans` : `/all_artisans`;
      const response = await fetch(`http://127.0.0.1:5000${endpoint}`, {
        method: distance ? "POST" : "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        ...(distance && { body: JSON.stringify({ distance }) }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch artisans");
      }

      const data = await response.json();
      setArtisans(data);
    } catch (error) {
      console.error("Error fetching artisans:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchArtisans();
  }, [distance]);

  return (
    <div style={{ backgroundColor: "beige", margin: ".5rem", padding: "1rem" }}>
      <Button
          variant="contained"
          size="small"
          style={{ marginTop: "0.5rem" }}
          onClick={() => window.location.href = "/client"}
        >
        Go to Artisans List
      </Button>
      {/* Search Section */}
      <Typography variant="h4" style={{ textAlign: "center", marginBottom: "1rem" }}>
        Search Artisan
      </Typography>
      <TextField
        style={{ width: "100%", marginBottom: "1rem" }}
        variant="outlined"
        label="Search for Artisan"
      />
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "1rem",
        }}
      >
        <Typography variant="h6">Distance: {distance ? `${distance} km` : ""}</Typography>
        <Slider
          value={distance}
          min={1}
          max={100}
          step={1}
          onChangeCommitted={(e, newValue) => setDistance(newValue)}
          style={{ width: "75%" }}
        />
      </div>
      <div style={{ display: "flex", gap: "1rem" }}>
        <Button
          style={{ flex: 1 }}
          variant="outlined"
          onClick={() => setDistance()}
        >
          <RestartAltIcon />
          Reset
        </Button>
        <Button style={{ flex: 1 }} variant="contained" onClick={fetchArtisans}>
          <SearchIcon />
          Search
        </Button>
      </div>

      {/* Map Section */}
      <MapContainer
        center={[51.505, -0.09]}
        zoom={13}
        scrollWheelZoom={false}
        style={{ height: "400px", marginTop: "1rem" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {artisans.map((artisan, index) => (
          <Marker key={index} position={[artisan.latitude, artisan.longitude]}>
            <Popup>
              <Typography variant="subtitle1">{artisan.username}</Typography>
              <Button
                variant="contained"
                size="small"
                style={{ marginTop: "0.5rem" }}
                onClick={() => setSelectedArtisan(artisan)}
              >
                Show
              </Button>
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      {/* Artisan Info Modal */}
      <Modal
        open={!!selectedArtisan}
        onClose={() => setSelectedArtisan(null)}
        aria-labelledby="artisan-info-title"
        aria-describedby="artisan-info-description"
      >
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: 400,
            bgcolor: "background.paper",
            border: "2px solid #000",
            boxShadow: 24,
            p: 4,
          }}
        >
          {selectedArtisan && (
            <ArtisanInfo key={selectedArtisan.id} artisan={selectedArtisan} />
          )}
          <Button
            variant="outlined"
            onClick={() => setSelectedArtisan(null)}
            style={{ marginTop: "10px", width: "100%" }}
          >
            Close
          </Button>
        </Box>
      </Modal>
    </div>
  );
};

export default Map;
