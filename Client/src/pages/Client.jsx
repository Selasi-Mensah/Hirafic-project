import React, { useState, useEffect } from 'react';
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

const Client = () => {
  const [bookings, setBookings] = useState([]);
  const [artisans, setArtisans] = useState([]);
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
  const name = sessionStorage.getItem('username');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const fetchData = async (endpoint, setter, loadingKey, errorKey) => {
    try {
      setLoading(prev => ({ ...prev, [loadingKey]: true }));
      setError(prev => ({ ...prev, [errorKey]: null }));
      
      const response = await fetch(`http://127.0.0.1:5000${endpoint}`, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setter(data);
    } catch (err) {
      setError(prev => ({ 
        ...prev, 
        [errorKey]: err.message || 'An error occurred'
      }));
    } finally {
      setLoading(prev => ({ ...prev, [loadingKey]: false }));
    }
  };

  useEffect(() => {
    fetchData('/bookings', setBookings, 'bookings', 'bookings');
    fetchData('/all_artisans', setArtisans, 'artisans', 'artisans');
    fetchData('/client', setProfile, 'profile', 'profile');
  }, []);

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
      setProfile(response.data);
      alert('Profile updated successfully');
    } catch (err) {
      setError({ profile: err.message });
    } finally {
      setLoading({ profile: false });
    }
  };

  const filteredArtisans = selectedProfession === 'all'
    ? artisans
    : artisans.filter(artisan => artisan.specialization === selectedProfession);

  const handleLogout = () => {
    window.location.href = '/logout';
  };

  const handleAbout = () => {
    window.location.href = '/About';
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Sidebar */}
        {isSidebarOpen && (
          <aside className="bg-gray-900 w-40 min-h-screen px-6 py-8 transition-all duration-300 fixed top-0 left-0 z-20">
            <h2 className="text-l text-center font-bold text-white mb-8">Navigation</h2>
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
            {isSidebarOpen ? 'Close Sidebar' : 'Open Sidebar'}
          </button>

          <div className="text-center justify-between items-center mb-8">
            {/* Welcome Message */}
            <h1 className="text-3xl font-bold mb-4 md:mb-0 text-gray-100">
              Welcome, {name}
            </h1>
            <p className="text-gray-400 text-lg mb-8">
              This is your home page. Use the navigation menu to explore.
            </p>
          </div>

          <Tabs defaultValue="bookings" className="space-y-3">
            <div className="text-center">
              <TabsList className="bg-gray-900 te">
                <TabsTrigger value="profile" className="data-[state=active]:bg-gray-800">
                  Profile
                </TabsTrigger>
                <TabsTrigger value="bookings" className="data-[state=active]:bg-gray-800">
                  Bookings
                </TabsTrigger>
                <TabsTrigger value="artisans" className="data-[state=active]:bg-gray-800">
                  Find Artisan
                </TabsTrigger>
              </TabsList>
            </div>

            <TabsContent value="profile">
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

            <TabsContent value="bookings">
              <div className="items-center justify-center gap-6 max-w-lg mx-auto">
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
            </TabsContent>

            <TabsContent value="artisans">
              <Card className="mb-6 bg-gray-900 border-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow max-w-lg mx-auto ">
                  <CardContent className="p-4">
                      <div className="gap-4 items-center justify-between ">
                          <div className="items-center gap-2">
                              <Select value={selectedProfession} onValueChange={setSelectedProfession}>
                              <SelectTrigger className="w-[180px] bg-gray-800 border-gray-700 text-gray-100">
                                  <Filter className="h-4 w-4 text-gray-200" />
                                  <SelectValue placeholder="Select a Profession" />
                              </SelectTrigger>
                              <SelectContent className="bg-gray-800 border-gray-700 text-gray-100">
                                  <SelectItem value="all">All Professions</SelectItem>
                                  <SelectItem value="Engineering">Engineering</SelectItem>
                                  <SelectItem value="Nursing">Nursing</SelectItem>
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
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </div>
  );
};

export default Client;