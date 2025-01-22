const ArtisanInfo = ({ artisan }) => {
    return (
      <div>
        <h2>{artisan.username}</h2>
        <p>Specialization: {artisan.specialization}</p>
        <p>Skills: {artisan.skills}</p>
        {/* Add more artisan details here */}
      </div>
    );
  };
  
  export default ArtisanInfo;