import React, { useState } from 'react';
import { Star, MapPin } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Dialog, DialogContent, DialogHeader, DialogTitle,DialogDescription, DialogClose } from '@/components/ui/dialog';
import ContactModal from '@/components/BookModal';

const ArtisanCard = ({ artisan }) => {
  const [isContactModalOpen, setIsContactModalOpen] = useState(false);
  const [isMoreModalOpen, setIsMoreModalOpen] = useState(false);

  const handleOpenContactModal = () => setIsContactModalOpen(true);
  const handleCloseContactModal = () => setIsContactModalOpen(false);

  const handleOpenMoreModal = () => setIsMoreModalOpen(true);
  const handleCloseMoreModal = () => setIsMoreModalOpen(false);

  return (
    <>
      <Card className="bg-gray-900 border-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow">
        <CardContent className="p-4 relative">
          <div className="flex items-start gap-4">
            {/* Avatar Section */}
            <Avatar className="h-14 w-14">
              <AvatarImage
                src={`http://localhost:5000/static/profile_pics/${artisan.image_file}`}
                alt={artisan.name}
              />
              <AvatarFallback className="bg-gray-700 text-gray-300 text-sm font-bold">
                {artisan.username.split(' ').map((n) => n[0]).join('')}
              </AvatarFallback>
            </Avatar>

            {/* Artisan Details */}
            <div className="flex-1">
              {/* Header */}
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                    {artisan.username}
                    <span className="text-sm bg-blue-600 text-white px-2 py-1 rounded-lg">
                      {artisan.hourlyRate}/hr
                    </span>
                  </h3>
                  <p className="text-sm text-gray-400 capitalize">{artisan.profession}</p>
                </div>
                <div className="flex items-center gap-1">
                  <Star className="h-4 w-4 text-yellow-500" />
                  <span className="text-sm text-gray-400">
                    {artisan.rating} ({artisan.reviews} reviews)
                  </span>
                </div>
              </div>

              {/* Additional Information */}
              <div className="mt-2">
                <p className="text-sm text-gray-400">
                  <span className="font-medium text-gray-300">Specialization:</span>{' '}
                  {artisan.specialization}
                </p>
                <div className="flex items-center gap-1 mt-1">
                  <MapPin className="h-4 w-4 text-gray-400" />
                  <span className="text-sm text-gray-400">{artisan.location}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Actions (Bottom-Right) */}
          <div className="absolute bottom-4 right-4 flex gap-2">
            <Button
              variant="outline"
              size="sm"
              className="border-gray-700 text-gray-800 hover:bg-gray-800"
              onClick={handleOpenMoreModal}
            >
              Skills
            </Button>
            <Button
              size="sm"
              className="bg-blue-600 hover:bg-blue-700 text-white"
              onClick={handleOpenContactModal}
            >
              Book Artisan
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Contact Modal */}
      <ContactModal artisan={artisan} isOpen={isContactModalOpen} onClose={handleCloseContactModal} />

      {/* More Modal */}
      <Dialog open={isMoreModalOpen} onOpenChange={handleCloseMoreModal}>
        <DialogContent aria-describedby="skills_details" className="bg-gray-900 border border-gray-800 rounded-lg shadow-lg">
          <DialogHeader>
            <DialogTitle className="text-lg font-bold text-white">Artisan {artisan.username} Skills</DialogTitle>
            <DialogDescription id="skills_details">
              Skills for {artisan.specialization === null || artisan.skills.trim().length === 0 ? artisan.specialization : "artisan's"} profession
            </DialogDescription>
          </DialogHeader>
          <div className="mt-4">
            {artisan.skills === null || artisan.skills.trim().length === 0 ? (
              <p className="text-sm text-gray-300 leading-relaxed">
                {artisan.skills}
              </p>
            ) : (
              <p className="text-sm text-gray-400">
                This artisan has not listed any skills yet.
              </p>
            )}
          </div>
          <div className="flex justify-end mt-6">
            <DialogClose asChild>
              <Button className="bg-gray-800 text-gray-300 hover:bg-gray-700 px-4 py-2 rounded-lg">
                Close
              </Button>
            </DialogClose>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default ArtisanCard;

