import { useState, useEffect, act } from 'react';
import axios from 'axios';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import ProfileSection from '@/components/ProfileSection';
import LoadingState from '@/components/LoadingState';
import ErrorState from '@/components/ErrorState';
import BookingCard from '@/components/BookingCard';
import ArtisanCard from '@/components/ArtisanCard';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent } from '@/components/ui/card';
import { Filter } from 'lucide-react';
import CloseIcon from '@mui/icons-material/Close';
import MenuOpenIcon from '@mui/icons-material/MenuOpen';
import Hirafic from '@/assets/Hirafic.jpg';

const Client = () => {
  const [bookings, setBookings] = useState([]);
  const [bookingsPagination, setBookingPage] = useState({
    bookings: [],
    total_pages: 0,
    current_page: 0
  })
  const [artisans, setArtisans] = useState([]);
  const [artisansPagination, setArtisanPage] = useState({
    artisans: [],
    total_pages: 0,
    current_page: 0
  })
  const [profile, setProfile] = useState({
    username: '',
    email: '',
    phone_number: '',
    location: '',
    image_file: ''
  });
  const [loading, setLoading] = useState({
    bookings: true,
    artisans: true,
    profile: true
  });
  const [error, setError] = useState({
    bookings: null,
    artisans: null,
    profile: null
  });
  const [selectedProfession, setSelectedProfession] = useState('all');
  const [file, setFile] = useState(null);
  const token = sessionStorage.getItem('access_token');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [distance, setDistance] = useState('');
  const [page, setPage] = useState(1);
  const [artisansPage, setArtisansPage] = useState(1);
  const per_page = 3;
  const [activeTab, setActiveTab] = useState('');

  const fetchData = async (endpoint, setter, loadingKey, errorKey, options = {}) => {
    try {
      setLoading(prev => ({ ...prev, [loadingKey]: true }));
      setError(prev => ({ ...prev, [errorKey]: null }));

      // Build query parameters if provided
      const queryParams = options.params
      ? '?' + new URLSearchParams(options.params).toString()
      : '';
      
      const response = await fetch(`http://127.0.0.1:5000${endpoint}${queryParams}`, {
        method: options.method || 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        ...(options.body && { body: JSON.stringify(options.body) }),
      });
      if (response.status === 401) {
        if (sessionStorage.getItem('access_token')) {
          sessionStorage.removeItem('access_token');
          sessionStorage.clear();
          window.location.href = '/login';
          alert('Session expired. Please login again');
          return;
        }
        else {
          return;
        }
      }
      else if (response.status !== 200) {
        alert('An error occurred');
      }
      const data = await response.json();
      setter(data);
    } catch (err) {
      setError(prev => ({ 
        ...prev, 
        [errorKey]: err.message || 'An error occurred',
      }));

    } finally {
      setLoading(prev => ({ ...prev, [loadingKey]: false }));
    }
  };
  
  // Handle tab change to refresh data
  const handleTabChange = (tab) => {
      // console.log('Tab changed to:', tab);
      setActiveTab(tab);
  };

  useEffect(() => {
    if (activeTab === 'profile') {
      // Fetch client profile (static endpoints)
      fetchData('/client', setProfile, 'profile', 'profile');
    }
    }, [activeTab]);

  useEffect(() => {
    if (activeTab === 'bookings' || activeTab === '') {
      // Fetch paginated bookings for client
      fetchData('/bookings', (response) => {
        // Extract and set pagination details
        setBookingPage((prev) => ({
          ...prev,
          bookings: response.bookings,
          current_page: response.current_page,
          total_pages: response.total_pages,
        }));
        setBookings(response.bookings);
      }, 'bookings', 'bookings', {
        params: {page: page, per_page: per_page},
      });
    }
  }, [activeTab, page, per_page]);

  useEffect(() => {
    if (activeTab === 'artisans' || activeTab === '') {
      // Dynamic endpoint for artisans
      const endpoint = distance ? '/nearby_artisans' : '/all_artisans';
      const options = distance ? {
        method: 'POST',
        body: {distance},
        params: {page: artisansPage, per_page: per_page}
      } : {params: {page: artisansPage, per_page: per_page}};
      fetchData(endpoint, (response) => {
        // Extract and set pagination detail
        setArtisanPage((prev) => ({
          ...prev,
          artisans: response.artisans,
          current_page: response.current_page,
          total_pages: response.total_pages,
        }));
        setArtisans(response.artisans);
      }, 'artisans', 'artisans', options);
    }
  }, [activeTab, distance, artisansPage, per_page]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile((prevProfile) => ({
      ...prevProfile,
      [name]: value,
    }));
  };
  
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading({ profile: true });
    setError({ profile: null });

    const formData = new FormData();
    formData.append('username', profile.username);
    formData.append('email', profile.email);
    formData.append('phone_number', profile.phone_number);
    formData.append('location', profile.location);
    if (file) {
      formData.append('picture', file);
    }
    console.log(formData);
    try {
      const response = await axios.post('http://127.0.0.1:5000/client', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      if (response.status === 401) {
        if (sessionStorage.getItem('access_token')) {
          sessionStorage.removeItem('access_token');
          sessionStorage.clear();
          window.location.href = '/login';
          alert('Session expired. Please login again');
          return;
        }
        else {
          return;
        }
      }
      setProfile(response.data);
      alert('Profile updated successfully');
    } catch (err) {
      setError({ profile: err.message });
    } finally {
      setLoading({ profile: false });
    }
  };

  const filteredArtisans = artisans 
  ? selectedProfession === 'all' 
    ? artisans 
    : artisans.filter(artisan => artisan.specialization === selectedProfession)
  : []; 

  const handleLogout = () => {
    sessionStorage.removeItem('access_token');
    sessionStorage.clear();
    window.location.href = '/login';
  };

  const handleAbout = () => {
    window.location.href = '/About';
  };

  const handlePageChange = (newPage) => setPage(newPage);
  const handleArtisansPageChange = (newPage) => setArtisansPage(newPage);

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 py-8 flex items-center justify-center">
      <div className="max-w-7xl mx-auto px-4">
        {/* Sidebar */}
        {isSidebarOpen && (
          <aside className="bg-gray-900 w-80 min-h-screen px-6 py-20 transition-all duration-300 fixed top-0 left-0 z-20">
            <h2 className="text-l text-center font-bold text-white mb-8">{name}</h2>
            <ul className="space-y-4">
              <li>
                <button
                  onClick={handleAbout}
                  className="w-full items-center gap-4 bg-gray-800 hover:bg-gray-700 text-white py-1 px-1 rounded-md transition-all duration-300"
                >
                  <span className="material-icons">About</span>
                </button>
              </li>
              <li>
                <button
                  onClick={handleLogout}
                  className="w-full items-center gap-4 bg-red-600 hover:bg-red-700 text-white py-1 px-1 rounded-md transition-all duration-300"
                >
                  <span className="material-icons">Logout</span>
                </button>
              </li>
            </ul>
          </aside>
        )}

        {/* Header */}
        <main className="items-center justify-center px-8 py-8">
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="bg-gray-800 text-white hover:bg-gray-700 px-4 py-2 rounded-md absolute top-4 left-4 z-10"
          >
            {/* {isSidebarOpen ? 'Close Sidebar' : 'Open Sidebar'} */}
          </button>
                    {/* Open Sidebar Button */}
                    <button
            onClick={() => setIsSidebarOpen(true)}
            className="bg-gray-800 text-white hover:bg-gray-700 p-3 rounded-md absolute top-4 left-4 z-10"
          >
            <MenuOpenIcon />
          </button>

          {/* Close Sidebar Button */}
          {isSidebarOpen && (
            <button
              onClick={() => setIsSidebarOpen(false)}
              className="bg-gray-800 text-white hover:bg-gray-700 p-4 rounded-md absolute top-4 left-2 z-50"
            >
              <CloseIcon />
            </button>
          )}


          {activeTab === '' && (
            <div className="text-center flex flex-col items-center">
              {/* Welcome Message */}
              <h2 className="text-3xl font-bold mb-4 text-gray-200">
                Welcome, {sessionStorage.getItem("username")}
              </h2>
              <p className="text-gray-400 text-lg mb-4">
                Use the navigation menu or select a tab to explore.
              </p>
            </div>
          )}
          {activeTab === 'profile' && (
           <div className="text-center flex flex-col items-center ">
              <h2 className="text-3xl font-bold mb-4 text-gray-200">My Profile</h2>
              <p className="text-gray-400 text-lg mb-4">
                Manage your account details and preferences here.
              </p>
              {/* <img
                src="/path/to/profile-placeholder.jpg" // Replace with an actual profile image path
                alt="Profile Placeholder"
                className="h-[150px] w-[150px] rounded-full shadow-md mb-4"
              /> */}
            </div>
          )}
          {activeTab === 'bookings' && (
            <div className="text-center flex flex-col items-center ">
              <h2 className="text-3xl font-bold mb-4 text-gray-200">Bookings Details</h2>
              <p className="text-gray-400 text-lg mb-4">
                View and manage your bookings here.
              </p>
            </div>
          )}
          {activeTab === 'artisans' && (
            <div className="font-poppins text-center flex flex-col items-center ">
              <h2 className="text-3xl font-bold mb-4 text-gray-200">Hirafic's Artisans</h2>
              <p className="text-gray-400 text-lg mb-4">
              Explore our skilled artisans and their profiles.
              </p>
          </div>
          )}
          

          <Tabs defaultValue={document.referrer.includes('/map') ? 'artisans' : 'bookings'}
            className="mx-auto"
            onValueChange={handleTabChange}
          >
            <div className="text-center"> 
              <TabsList className="flex bg-gray-900 text-gray-100 w-[315px] mx-auto gap-6 mb-4">
                <TabsTrigger value="profile" className="w-[200px] data-[state=active]:bg-gray-800 ">
                  Profile
                </TabsTrigger>
                <TabsTrigger value="bookings" className="w-[200px] data-[state=active]:bg-gray-800">
                  Bookings
                </TabsTrigger>
                <TabsTrigger value="artisans" className="w-[200px] data-[state=active]:bg-gray-800">
                  Find Artisan
                </TabsTrigger>
              </TabsList>
            </div>

            <TabsContent value="profile" key="profile">
              <ProfileSection
                profile={profile}
                loading={loading}
                error={error}
                handleSubmit={handleSubmit}
                handleChange={handleChange}
                handleFileChange={handleFileChange}
                editable={true}
              />
            </TabsContent>

            <TabsContent value="bookings" key="bookings">
              <div className="grid items-center justify-center max-w-lg mx-auto gap-2 ">
                {loading.bookings ? (
                  <LoadingState />
                ) : error.bookings ? (
                  <ErrorState message={error.bookings} />
                ) : bookings.length > 0 ? (
                  bookings.map(booking => (
                    <BookingCard key={booking.id} booking={booking} />
                  ))
                ) : (
                  <p className="text-center text-gray-400">No bookings found.</p>
                )}
              </div>
              <div className="flex items-center justify-center mt-4">
                  {bookingsPagination.current_page > 1 && (
                    <button 
                      className="px-4 py-2 bg-blue-600 text-white rounded-md mr-2"
                      onClick={() => handlePageChange(bookingsPagination.current_page - 1)}
                    >
                      Previous
                    </button>
                  )}
                  <span className="text-gray-400">
                    {bookingsPagination.total_pages != 0 ? (
                      <>Page {bookingsPagination.current_page} of {bookingsPagination.total_pages}</>
                    ) : (
                      <>Page 0 of 0</>
                    )}
                  </span>
                  {bookingsPagination.current_page < bookingsPagination.total_pages && (
                    <button 
                      className="px-4 py-2 bg-blue-600 text-white rounded-md ml-2"
                      onClick={() => handlePageChange(bookingsPagination.current_page + 1)}
                    >
                      Next
                    </button>
                  )}
                </div>
            </TabsContent>
            <TabsContent value="artisans" key="artisans">
              <Card className="grid mb-4 bg-gray-900 border-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow max-w-2xl mx-auto p-4">
                <CardContent className="flex flex-col gap-4">
                  <div className="flex flex-col md:flex-row items-center gap-6">
                    {/* Profession Selector */}
                    <div className="flex flex-col w-full md:w-auto items-center">
                      <Select value={selectedProfession} onValueChange={setSelectedProfession}>
                        <SelectTrigger
                          className="w-full md:w-[200px] bg-gray-800 border-gray-700 text-gray-100 flex items-center "
                          id="profession"
                        >
                          <Filter className="h-4 w-4 text-gray-200 mr-2" />
                          <SelectValue placeholder="Select a Profession" />
                        </SelectTrigger>
                        <SelectContent className="bg-gray-800 border-gray-700 text-gray-100">
                          <SelectItem value="all">All Professions</SelectItem>
                          <SelectItem value="Engineer">Engineer</SelectItem>
                          <SelectItem value="Nurse">Nurse</SelectItem>
                          <SelectItem value="Cleaner">Cleaner</SelectItem>
                          <SelectItem value="Technician">Technician</SelectItem>
                          <SelectItem value="Mechanic">Mechanic</SelectItem>
                          <SelectItem value="Painter">Painter</SelectItem>
                          <SelectItem value="Carpenter">Carpenter</SelectItem>
                          <SelectItem value="Plumber">Plumber</SelectItem>
                          <SelectItem value="Electrician">Electrician</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    {/* Distance Input */}
                    <div className="flex flex-col w-full md:w-auto items-center">
                      <input
                        type=""
                        id="distance"
                        name="distance"
                        value={distance}
                        onChange={(e) => setDistance(e.target.value)}
                        placeholder="Search distance (km)"
                        className="w-full md:w-[160px] md:h-[40px] bg-gray-800 border-gray-700 text-gray-100 placeholder:text-gray-200 text-sm px-2 rounded-md"
                      />
                    </div>

                    <div className="flex flex-col w-full md:w-auto items-center">
                      <button
                        onClick={() => window.location.href = '/map'}
                        className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md transition-all duration-300"
                      >
                        View on Map
                      </button>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <div className=" gap-6 items-center justify-center min-w-screen max-w-lg mx-auto">
                {loading.artisans ? (
                  <LoadingState />
                ) : error.artisans ? (
                  <ErrorState message={error.artisans} />
                ) : filteredArtisans.length > 0 ? (
                  filteredArtisans.map(artisan => (
                    <ArtisanCard key={artisan.id} artisan={artisan} />
                  ))
                ) : (
                  <p className="text-center text-gray-400 col-span-2">No artisans found.</p>
                )}
              </div>
              <div className="flex items-center justify-center mt-4">
                  {artisansPagination.current_page > 1 && (
                    <button 
                      className="px-4 py-2 bg-blue-600 text-white rounded-md mr-2"
                      onClick={() => handleArtisansPageChange(artisansPagination.current_page - 1)}
                    >
                      Previous
                    </button>
                  )}
                  <span className="text-gray-400">
                    {artisansPagination.total_pages != 0 ? (
                      <>Page {artisansPagination.current_page} of {artisansPagination.total_pages}</>
                    ) : (
                      <>Page 0 of 0</>
                    )}
                  </span>
                  {artisansPagination.current_page < artisansPagination.total_pages && (
                    <button 
                      className="px-4 py-2 bg-blue-600 text-white rounded-md ml-2"
                      onClick={() => handleArtisansPageChange(artisansPagination.current_page + 1)}
                    >
                      Next
                    </button>
                  )}
                </div>
            </TabsContent>
          </Tabs>
        </main>
        <p className="absolute top-4 right-4 flex items-center justify-center h-[80px] w-[80px] bg-white rounded-full shadow-lg transition-transform hover:scale-105 hover:shadow-xl">
          <img
            className="h-[75px] w-[75px] object-cover rounded-full"
            src={Hirafic}
            alt="Logo"
          />
        </p>
      </div>
    </div>
  );
};

export default Client;