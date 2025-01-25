import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogClose } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const BookModal = ({ booking, isOpen, onClose }) => {
    const [issue, setIssue] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
    
        try {
            console.log(sessionStorage.getItem('email'));
            const response = await axios.get('http://127.0.0.1:5000/report', {
            params: {
                artisan_name: booking.artisan_name,
                client_name: booking.client_name,
                issue: issue,
                booking_id: booking.id
            },
            headers: {
                Authorization: `Bearer ${sessionStorage.getItem('access_token')}`,
                'Content-Type': 'application/json',
            },
            });
            alert('Report Sent to Hirafic Team Successfully');
            onClose();
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };
    
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="bg-gray-900 border border-gray-700 shadow-lg rounded-lg">
        <DialogHeader>
          <DialogTitle className="text-lg font-bold text-white">Report {booking.artisan_name} Artisan</DialogTitle>
          <DialogDescription className="text-sm text-gray-400">
            Report Artisan to Hirafic Team
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-6">
            {/* Details Textarea */}
            <textarea
              className="w-full p-3 bg-gray-800 text-gray-100 border border-gray-700 rounded-lg focus:outline-none focus:ring focus:ring-blue-500"
              rows="5"
              placeholder="Write your issue with the artisan in details..."
              value={issue}
              onChange={(e) => setIssue(e.target.value)}
              required
            />
          <div className="flex justify-end space-x-2">
            {/* Submit Button */}
            <Button
              type="submit"
              className={`px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 focus:outline-none focus:ring focus:ring-blue-500 ${
                loading ? 'opacity-50 cursor-not-allowed' : ''
              }`}
              disabled={loading}
            >
              {loading ? 'Sending...' : 'Report Now'}
            </Button>
            {/* Close Button */}
            <DialogClose asChild>
              <Button
                variant="outline"
                className="px-4 py-2 bg-gray-800 text-gray-300 border border-gray-700 rounded-lg hover:bg-gray-700 focus:outline-none focus:ring focus:ring-gray-500"
              >
                Close
              </Button>
            </DialogClose>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default BookModal;
