import React, { useState } from 'react';
import { Calendar, MessageSquare } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const BookingCard = ({ booking }) => {
  const [refreshCount, setRefreshCount] = useState(0);

  const handleRefresh = () => {
    setRefreshCount(refreshCount + 1);
  };

  return (
    <Card className="bg-gray-900 border-gray-800" onClick={handleRefresh}>
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
};

export default BookingCard;
