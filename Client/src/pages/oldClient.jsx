import React, { useState, useEffect } from 'react';
import { Star, MapPin, MessageSquare, Calendar, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import axios from 'axios';

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
      const response = await axios.post('http://127.0.0.1:5000/client', profile, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
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

  const LoadingState = () => (
    <div className="flex justify-center items-center p-8">
      <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
    </div>
  );

  const ErrorState = ({ message }) => (
    <div className="text-red-400 p-4 text-center bg-red-900/20 rounded-lg">
      {message}
    </div>
  );

  const ProfileSection = ({ editable }) => (
    <div className="bg-gray-900 text-gray-100 p-6 rounded-lg shadow-md max-w-md mx-auto">
      {loading.profile ? <LoadingState /> : error.profile ? <ErrorState message={error.profile} /> : (
        <form onSubmit={handleSubmit} className="text-center">
          <div className="pb-4">
            <img
              src={profile?.image_file ? `http://localhost:5000/static/profile_pics/${profile.image_file}` : "http://localhost:5000/static/profile_pics/default.jpg"}
              alt="Profile"
              className="w-32 h-32 rounded-full mx-auto"
            />
          </div>
          <div className="space-y-3">
            {editable ? (
              <>
                <div className="pb-2">
                  <label className="text-xs text-gray-400">Name</label>
                  <input
                    type="text"
                    name="username"
                    value={profile?.username || ''}
                    onChange={handleChange}
                    className="w-full p-2 bg-gray-800 text-gray-100 rounded"
                  />
                </div>
                <div className="pb-2">
                  <label className="text-xs text-gray-400">Email</label>
                  <input
                    type="email"
                    name="email"
                    value={profile?.email || ''}
                    onChange={handleChange}
                    className="w-full p-2 bg-gray-800 text-gray-100 rounded"
                  />
                </div>
                <div className="pb-2">
                  <label className="text-xs text-gray-400">Phone</label>
                  <input
                    type="text"
                    name="phone_number"
                    value={profile?.phone_number || ''}
                    onChange={handleChange}
                    className="w-full p-2 bg-gray-800 text-gray-100 rounded"
                  />
                </div>
                <div className="pb-2">
                  <label className="text-xs text-gray-400">Location</label>
                  <input
                    type="text"
                    name="location"
                    value={profile?.location || ''}
                    onChange={handleChange}
                    className="w-full p-2 bg-gray-800 text-gray-100 rounded"
                  />
                </div>
                <div className="flex justify-center mt-4">
                  <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
                    Update Profile
                  </Button>
                </div>
              </>
            ) : (
              <>
                <div className="pb-2">
                  <p className="text-xs text-gray-400">Name</p>
                  <p className="text-sm">{profile?.username || 'No name provided'}</p>
                </div>
                <div className="pb-2">
                  <p className="text-xs text-gray-400">Email</p>
                  <p className="text-sm">{profile?.email || 'No email provided'}</p>
                </div>
                <div className="pb-2">
                  <p className="text-xs text-gray-400">Phone</p>
                  <p className="text-sm">{profile?.phone_number || 'No phone number provided'}</p>
                </div>
                <div className="pb-2">
                  <p className="text-xs text-gray-400">Location</p>
                  <p className="text-sm">{profile?.location || 'No location provided'}</p>
                </div>
              </>
            )}
          </div>
        </form>
      )}
    </div>
  );

  const BookingCard = ({ booking }) => (
    <Card className="bg-gray-900 border-gray-800">
      <CardContent className="p-6">
        <div className="flex flex-col md:flex-row justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-xl font-semibold mb-1 text-gray-100">{booking.artisan_name}</h3>
                <p className="text-gray-400">{booking.details}</p>
              </div>
              <Badge 
                variant={booking.status === 'Completed' ? 'secondary' : 'default'}
                className="bg-blue-600"
              >
                {booking.status}
              </Badge>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-gray-400" />
              <span className="text-sm text-gray-400">
                {new Date(booking.request_date).toLocaleDateString()} - 
                {new Date(booking.completion_date).toLocaleDateString()}
              </span>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" className="border-gray-700 hover:bg-gray-800">
              View Details
            </Button>
            <Button variant="outline" className="border-gray-700 hover:bg-gray-800">
              <MessageSquare className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  const ArtisanCard = ({ artisan }) => (
    <Card className="bg-gray-900 border-gray-800">
      <CardContent className="p-6">
        <div className="flex gap-4">
          <Avatar className="h-16 w-16">
            <AvatarImage src={`http://localhost:5000/static/profile_pics/${artisan.image_file}`} alt={artisan.name} />
            <AvatarFallback className="bg-gray-800">
              {artisan.name.split(' ').map(n => n[0]).join('')}
            </AvatarFallback>
          </Avatar>
          <div className="flex-1">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-semibold text-gray-100">{artisan.name}</h3>
                <p className="text-sm text-gray-400">{artisan.profession}</p>
              </div>
              <Badge variant="outline" className="border-gray-700">
                {artisan.hourlyRate}/hr
              </Badge>
            </div>
            <div className="flex flex-wrap gap-4 mt-2">
              <div className="flex items-center gap-1">
                <MapPin className="h-4 w-4 text-gray-400" />
                <span className="text-sm text-gray-400">{artisan.location}</span>
              </div>
              <div className="flex items-center gap-1">
                <Star className="h-4 w-4 text-yellow-500" />
                <span className="text-sm text-gray-400">
                  {artisan.rating} ({artisan.reviews} reviews)
                </span>
              </div>
            </div>
            <div className="flex justify-between items-center mt-4">
              <span className="text-sm text-gray-400">{artisan.availability}</span>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" className="border-gray-700 hover:bg-gray-800">
                  View Profile
                </Button>
                <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                  Contact
                </Button>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center mb-8"></div>
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
            <ProfileSection editable={true} />
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
  );
};

export default Client;