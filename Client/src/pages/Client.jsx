import React, { useState } from 'react';
import { Search, Filter, Star, MapPin, MessageSquare, Calendar, Plus, Moon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const ClientDashboardDark = () => {
  const [projects, setProjects] = useState([
    {
      id: 1,
      title: 'Kitchen Renovation',
      artisan: 'John Doe',
      artisanProfession: 'Carpenter',
      status: 'In Progress',
      startDate: '2024-01-15',
      endDate: '2024-02-15',
    },
    {
      id: 2,
      title: 'Bathroom Plumbing',
      artisan: 'Jane Smith',
      artisanProfession: 'Plumber',
      status: 'Completed',
      startDate: '2024-01-01',
      endDate: '2024-01-10',
    }
  ]);

  const [artisans] = useState([
    {
      id: 1,
      name: 'John Doe',
      profession: 'Carpenter',
      location: 'New York, NY',
      rating: 4.8,
      reviews: 156,
      hourlyRate: '$45',
      availability: 'Available',
      image: '/api/placeholder/100/100'
    },
    {
      id: 2,
      name: 'Jane Smith',
      profession: 'Plumber',
      location: 'Brooklyn, NY',
      rating: 4.9,
      reviews: 203,
      hourlyRate: '$55',
      availability: 'Booked until Feb 1',
      image: '/api/placeholder/100/100'
    }
  ]);

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center mb-8">
          <h1 className="text-3xl font-bold mb-4 md:mb-0 text-gray-100">Welcome, Alex</h1>
          <Button className="gap-2 bg-blue-600 hover:bg-blue-700">
            <Plus className="h-4 w-4" />
            Post New Project
          </Button>
        </div>

        <Tabs defaultValue="projects" className="space-y-6">
          <TabsList className="bg-gray-900">
            <TabsTrigger value="projects" className="data-[state=active]:bg-gray-800">My Projects</TabsTrigger>
            <TabsTrigger value="find" className="data-[state=active]:bg-gray-800">Find Artisans</TabsTrigger>
          </TabsList>

          <TabsContent value="projects">
            <div className="grid gap-6">
              {projects.map((project) => (
                <Card key={project.id} className="bg-gray-900 border-gray-800">
                  <CardContent className="p-6">
                    <div className="flex flex-col md:flex-row justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-start justify-between mb-4">
                          <div>
                            <h3 className="text-xl font-semibold mb-1 text-gray-100">{project.title}</h3>
                            <p className="text-gray-400">Artisan: {project.artisan} ({project.artisanProfession})</p>
                          </div>
                          <Badge 
                            variant={project.status === 'Completed' ? 'secondary' : 'default'}
                            className="bg-blue-600"
                          >
                            {project.status}
                          </Badge>
                        </div>
                        <div className="flex flex-wrap gap-4">
                          <div className="flex items-center gap-2">
                            <Calendar className="h-4 w-4 text-gray-400" />
                            <span className="text-sm text-gray-400">
                              {new Date(project.startDate).toLocaleDateString()} - 
                              {new Date(project.endDate).toLocaleDateString()}
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
              ))}
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
              {artisans.map((artisan) => (
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
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default ClientDashboardDark;