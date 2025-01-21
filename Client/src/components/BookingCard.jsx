import React, { useState } from 'react';
import { Calendar } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogClose } from '@/components/ui/dialog';

const BookingCard = ({ booking }) => {
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const userRole = sessionStorage.getItem('role');

  const toggleDetailsModal = () => {
    setIsDetailsOpen(!isDetailsOpen);
  };

  const handleBookingAction = async (action) => {
    try {
      const response = await fetch('/book_artisan', {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem('access_token')}`,
          'Content-Type': 'application/json' },
        body: JSON.stringify({ bookingId: booking.id, action }),
      });
      if (!response.ok) {
        throw new Error('Failed to update booking status.');
      }
      alert(`${action.charAt(0).toUpperCase() + action.slice(1)} action successful.`);
    } catch (error) {
      console.error(error);
      alert('An error occurred while processing your request.');
    }
  };

  const getStatusBadgeColor = (status) => {
    switch (status) {
      case 'Pending':
        return 'bg-yellow-600 text-yellow-100';
      case 'Accepted':
        return 'bg-green-600 text-green-100';
      case 'Rejected':
        return 'bg-red-600 text-red-100';
      case 'Completed':
        return 'bg-blue-600 text-blue-100';
      default:
        return 'bg-gray-600 text-gray-100';
    }
  };

  return (
    <>
      {/* Booking Card */}
      <Card className="bg-gray-900 border-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow w-full sm:w-80">
        <CardContent className="pl-4 pr-6 py-4">
          <div className="flex flex-col md:flex-row justify-between gap-4">
            <div className="flex-1">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h4 className="text-xl font-semibold mb-1 text-gray-100">{booking.title}</h4>
                </div>
                <Badge className={`${getStatusBadgeColor(booking.status)} px-2 py-1 rounded`}>
                  {booking.status}
                </Badge>
              </div>
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-gray-400" />
                  <span className="text-sm text-gray-400">
                    {new Date(booking.request_date).toLocaleDateString()} -{' '}
                    {new Date(booking.completion_date).toLocaleDateString()}
                  </span>
                </div>
                <div className="items-right justify-right gap-2">
                  <Button
                    variant="outline"
                    className="border-gray-700 hover:bg-gray-800"
                    onClick={toggleDetailsModal}
                    >
                      View Details
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Details Modal */}
      <Dialog open={isDetailsOpen} onOpenChange={toggleDetailsModal}>
        <DialogContent className="bg-gray-900 border border-gray-800 shadow-lg rounded-lg">
          <DialogHeader>
            <DialogTitle className="text-lg font-bold text-white">Booking Details</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-400 mb-1">Title</p>
              <p className="text-base text-gray-100">{booking.title}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">Status</p>
              <p className="text-base text-gray-100">{booking.status}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">{userRole === "Artisan" ? "Client Name" : "Artisan Name"}</p>
              <p className="text-base text-gray-100">{userRole === "Artisan" ? booking.client_name : booking.artisan_name}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">Details</p>
              <p className="text-base text-gray-100">{booking.details}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">Submission Date</p>
              <p className="text-base text-gray-100">
                {new Date(booking.request_date).toLocaleDateString()}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">Completion Date</p>
              <p className="text-base text-gray-100">
                {new Date(booking.completion_date).toLocaleDateString()}
              </p>
            </div>
          </div>
          <div className="flex justify-end mt-6">
            <DialogClose asChild>
              <Button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
                Close
              </Button>
            </DialogClose>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default BookingCard;
