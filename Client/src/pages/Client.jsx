import React, { useState, useEffect } from 'react';
import { Search, Filter, Star, MapPin, MessageSquare, Calendar, Plus, Moon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import axios from 'axios';

const ClientDashboardDark = () => {
  const [bookings, setbookings] = useState([]);
  const [artisans, setArtisans] = useState([]);
  const [profile, setProfile] = useState();
  const token = sessionStorage.getItem('access_token');
  const name = sessionStorage.getItem('username');

  // Fetch bookings (bookings) from backend
  useEffect(() => {
    const fetchbookings = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/bookings', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        console.log(response.data);
        setbookings(response.data);
      } catch (error) {
        console.error('Error fetching bookings:', error);
      }
    };

    fetchbookings();
  }, [token]);

  // Fetch nearby artisans from backend
  useEffect(() => {
    const fetchArtisans = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/all_artisans', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        console.log(response.data);
        setArtisans(response.data);
      } catch (error) {
        console.error('Error fetching artisans:', error);
      }
    };

    fetchArtisans();
  }, [token]);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/client', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        console.log(response.data);
        setProfile(response.data);
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };

    fetchProfile();
  }, [token]);

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center mb-8">
          <h1 className="text-3xl font-bold mb-4 md:mb-0 text-gray-100">Welcome, {name} </h1>
          <Button className="gap-2 bg-blue-600 hover:bg-blue-700">
            <Plus className="h-4 w-4" />
            Post New booking
          </Button>
        </div>

        <Tabs defaultValue="profile" className="space-y-6">
          <TabsList className="bg-gray-900">
            <TabsTrigger value="profile" className="data-[state=active]:bg-gray-800">Profile</TabsTrigger>
            <TabsTrigger value="bookings" className="data-[state=active]:bg-gray-800">Bookings</TabsTrigger>
            <TabsTrigger value="find" className="data-[state=active]:bg-gray-800">Find Artisan</TabsTrigger>
          </TabsList>

          <TabsContent value="profile">
          <div className="bg-gray-900 text-gray-100 p-6 rounded-lg shadow-md max-w-sm mx-auto">
            <div className="space-y-4">
              <div className="border-b border-gray-700 pb-2">
                <p className="text-sm text-gray-400">Name</p>
                <p className="text-lg">{profile?.name || "Anonymous User"}</p>
              </div>
              <div className="border-b border-gray-700 pb-2">
                <p className="text-sm text-gray-400">Email</p>
                <p className="text-lg">{profile?.email || "No email provided"}</p>
              </div>
              <div className="border-b border-gray-700 pb-2">
                <p className="text-sm text-gray-400">Phone Number</p>
                <p className="text-lg">{profile?.phone_number || "No phone number provided"}</p>
              </div>
              <div className="border-b border-gray-700 pb-2">
                <p className="text-sm text-gray-400">Location</p>
                <p className="text-lg">{profile?.location || "No location provided"}</p>
              </div>
              <div className="pb-2">
                <p className="text-sm text-gray-400">Profile Picture</p>
                <img
                  src={profile?.image_file || "/default-profile.png"}
                  alt="Profile"
                  className="w-full h-auto rounded-lg"
                />
              </div>
            </div>
          </div>
          </TabsContent> 

          <TabsContent value="bookings">
            <div className="grid gap-6">
              {bookings.length > 0 ? (
                bookings.map((booking) => (
                  <Card key={booking.id} className="bg-gray-900 border-gray-800">
                    <CardContent className="p-6">
                      <div className="flex flex-col md:flex-row justify-between gap-4">
                        <div className="flex-1">
                          <div className="flex items-start justify-between mb-4">
                            <div>
                              <h3 className="text-xl font-semibold mb-1 text-gray-100">{booking.artisan_name}</h3>
                              <p className="text-gray-400">Artisan: {booking.details}</p>
                            </div>
                            <Badge 
                              variant={booking.status === 'Completed' ? 'secondary' : 'default'}
                              className="bg-blue-600"
                            >
                              {booking.status}
                            </Badge>
                          </div>
                          <div className="flex flex-wrap gap-4">
                            <div className="flex items-center gap-2">
                              <Calendar className="h-4 w-4 text-gray-400" />
                              <span className="text-sm text-gray-400">
                                {new Date(booking.request_date).toLocaleDateString()} - 
                                {new Date(booking.completion_date).toLocaleDateString()}
                              </span>
                            </div>
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <Button variant="outline" className="border-gray-700 hover:bg-gray-800">View Details</Button>
                          <Button variant="outline" className="border-gray-700 hover:bg-gray-800">
                            <MessageSquare className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))
              ) : (
                <p>No bookings found.</p>
              )}
            </div>
          </TabsContent>

          <TabsContent value="find">
            <Card className="mb-6 bg-gray-900 border-gray-800">
              <CardContent className="p-6">
                <div className="flex flex-col md:flex-row gap-4">
                  <div className="flex-1">
                    <div className="relative">
                      <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input 
                        placeholder="Search artisans..." 
                        className="pl-9 bg-gray-800 border-gray-700 text-gray-100 placeholder:text-gray-500"
                      />
                    </div>
                  </div>
                  <div className="flex gap-4">
                    <Select>
                      <SelectTrigger className="w-[180px] bg-gray-800 border-gray-700">
                        <SelectValue placeholder="Profession" />
                      </SelectTrigger>
                      <SelectContent className="bg-gray-800 border-gray-700">
                        <SelectItem value="carpenter">Carpenter</SelectItem>
                        <SelectItem value="plumber">Plumber</SelectItem>
                        <SelectItem value="electrician">Electrician</SelectItem>
                      </SelectContent>
                    </Select>
                    <Button variant="outline" className="gap-2 border-gray-700 hover:bg-gray-800">
                      <Filter className="h-4 w-4" />
                      Filters
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="grid md:grid-cols-2 gap-6">
              {artisans.length > 0 ? (
                artisans.map((artisan) => (
                  <Card key={artisan.id} className="bg-gray-900 border-gray-800">
                    <CardContent className="p-6">
                      <div className="flex gap-4">
                        <Avatar className="h-16 w-16">
                          <AvatarImage src={artisan.image} alt={artisan.name} />
                          <AvatarFallback className="bg-gray-800">{artisan.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                        </Avatar>
                        <div className="flex-1">
                          <div className="flex justify-between items-start">
                            <div>
                              <h3 className="font-semibold text-gray-100">{artisan.name}</h3>
                              <p className="text-sm text-gray-400">{artisan.profession}</p>
                            </div>
                            <Badge variant="outline" className="border-gray-700">{artisan.hourlyRate}/hr</Badge>
                          </div>
                          <div className="flex flex-wrap gap-4 mt-2">
                            <div className="flex items-center gap-1">
                              <MapPin className="h-4 w-4 text-gray-400" />
                              <span className="text-sm text-gray-400">{artisan.location}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Star className="h-4 w-4 text-yellow-500" />
                              <span className="text-sm text-gray-400">{artisan.rating} ({artisan.reviews} reviews)</span>
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
                ))
              ) : (
                <p>No artisans found.</p>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default ClientDashboardDark;
