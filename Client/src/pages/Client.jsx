import React, { useState, useEffect } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import axios from 'axios';
import LoadingState from '@/components/LoadingState';
import ErrorState from '@/components/ErrorState';
import ProfileSection from '@/components/ProfileSection';
import BookingCard from '@/components/BookingCard';
import ArtisanCard from '@/components/ArtisanCard';
import { Card, CardContent } from '@/components/ui/card';

const Client = () => {
  const [bookings, setBookings] = useState([]);
  const [artisans, setArtisans] = useState([]);
  const [profile, setProfile] = useState(null);
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
  const [selectedProfession, setSelectedProfession] = useState('');
  const [file, setFile] = useState(null);
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };
  const token = sessionStorage.getItem('access_token');
  const name = sessionStorage.getItem('username');

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(prev => ({ ...prev, profile: true }));
    setError(prev => ({ ...prev, profile: null }));

    try {
      const formData = new FormData();
      formData.append('username', profile.username);
      formData.append('email', profile.email);
      formData.append('phone_number', profile.phone_number);
      formData.append('location', profile.location);
      formData.append('picture', file);

      const response = await axios.post('http://127.0.0.1:5000/client', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      setProfile(response.data);
      alert('Profile updated successfully');
    } catch (err) {
      setError(prev => ({ ...prev, profile: err.message }));
    } finally {
      setLoading(prev => ({ ...prev, profile: false }));
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center mb-8">
          <h1 className="text-3xl font-bold mb-4 md:mb-0 text-gray-100">
            Welcome, {name}
          </h1>
        </div>

        <Tabs defaultValue="profile" className="space-y-6">
          <TabsList className="bg-gray-900">
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
            <div className="grid gap-6">
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
            <Card className="mb-6 bg-gray-900 border-gray-800">
              <CardContent className="p-6">
                <div className="flex flex-col md:flex-row gap-4">
                  <div className="flex gap-4">
                    <Select value={selectedProfession} onValueChange={setSelectedProfession}>
                      <SelectTrigger className="w-[180px] bg-gray-800 border-gray-700">
                        <SelectValue placeholder="Profession" />
                      </SelectTrigger>
                      <SelectContent className="bg-gray-800 border-gray-700">
                        <SelectItem value="all">All Professions</SelectItem>
                        <SelectItem value="carpenter">Carpenter</SelectItem>
                        <SelectItem value="plumber">Plumber</SelectItem>
                        <SelectItem value="electrician">Electrician</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="grid md:grid-cols-2 gap-6">
              {loading.artisans ? (
                <LoadingState />
              ) : error.artisans ? (
                <ErrorState message={error.artisans} />
              ) : artisans.length > 0 ? (
                artisans.map(artisan => (
                  <ArtisanCard key={artisan.id} artisan={artisan} />
                ))
              ) : (
                <p className="text-center text-gray-400 col-span-2">No artisans found.</p>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Client;
