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

const Artisan = () => {
  const [bookings, setBookings] = useState([]);
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
    fetchData('/artisan', setProfile, 'profile', 'profile');
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile((prevProfile) => ({
      ...prevProfile,
      [name]: value,
    }));
  };

  const handleSubmit = async (e, selectedFile) => {
    e.preventDefault();
    setLoading({ profile: true });
    setError({ profile: null });

    const formData = new FormData();
    formData.append('username', profile.username);
    formData.append('email', profile.email);
    formData.append('phone_number', profile.phone_number);
    formData.append('location', profile.location);
    formData.append('skills', profile.skills);
    formData.append('specialization', profile.specialization);
    if (selectedFile) {
      formData.append('profile_image', selectedFile);
    }
    
    try {
      const response = await axios.post('http://127.0.0.1:5000/profile', formData, {
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

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center mb-8">
          <h1 className="text-3xl font-bold mb-4 md:mb-0 text-gray-100">
            Welcome, {name}
          </h1>
        </div>

        <Tabs defaultValue="bookings" className="space-y-3">
          <TabsList className="bg-gray-900 te">
            <TabsTrigger value="profile" className="data-[state=active]:bg-gray-800">
              Profile
            </TabsTrigger>
            <TabsTrigger value="bookings" className="data-[state=active]:bg-gray-800">
              Bookings
            </TabsTrigger>
          </TabsList>

          <TabsContent value="profile">
            <ProfileSection
              profile={profile}
              loading={loading}
              error={error}
              handleSubmit={handleSubmit}
              handleChange={handleChange}
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
        </Tabs>
      </div>
    </div>
  );
};

export default Artisan;