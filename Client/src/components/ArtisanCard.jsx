import React, { useState } from 'react';
import { Star, MapPin } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import ContactModal from '@/components/BookModal';

const ArtisanCard = ({ artisan }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  return (
    <>
      <Card className="bg-gray-900 border-gray-800">
        <CardContent className="p-6">
          <div className="flex gap-4">
            <Avatar className="h-16 w-16">
              <AvatarImage src={`http://localhost:5000/static/profile_pics/${artisan.image_file}`} alt={artisan.name} />
              <AvatarFallback className="bg-gray-800">
                {artisan.username.split(' ').map(n => n[0]).join('')}
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
                  <Button size="sm" className="bg-blue-600 hover:bg-blue-700" onClick={handleOpenModal}>
                    Book Artisan
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
      <ContactModal artisan={artisan} isOpen={isModalOpen} onClose={handleCloseModal} />
    </>
  );
};

export default ArtisanCard;