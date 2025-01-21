import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogClose } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const BookModal = ({ artisan, isOpen, onClose }) => {
  const [title, setTitle] = useState('');
  const [details, setDetails] = useState('');
  const [completionDate, setCompletionDate] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://127.0.0.1:5000/book_artisan', {
        artisan_email: artisan.email,
        client_email: sessionStorage.getItem('email'),
        title,
        completion_date: completionDate,
        details,
      }, {
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
        },
      });
      alert('Booking request sent successfully');
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
          <DialogTitle className="text-lg font-bold text-white">Book {artisan.username}</DialogTitle>
          <DialogDescription className="text-sm text-gray-400">
            Send a booking request to artisan
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            {/* Title Input */}
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-1">Title</label>
              <input
                type="text"
                className="w-full p-3 bg-gray-800 text-gray-100 border border-gray-700 rounded-lg focus:outline-none focus:ring focus:ring-blue-500"
                placeholder="Enter a title for your request..."
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>
            {/* Details Textarea */}
            <textarea
              className="w-full p-3 bg-gray-800 text-gray-100 border border-gray-700 rounded-lg focus:outline-none focus:ring focus:ring-blue-500"
              rows="5"
              placeholder="Your booking details here..."
              value={details}
              onChange={(e) => setDetails(e.target.value)}
              required
            />
            {/* Completion Date Picker */}
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-1">Expected Completion Date</label>
              <DatePicker
                selected={completionDate}
                onChange={(date) => setCompletionDate(date)}
                className="w-full p-3 bg-gray-800 text-gray-100 border border-gray-700 rounded-lg focus:outline-none focus:ring focus:ring-blue-500"
                dateFormat="yyyy/MM/dd"
                placeholderText="Select a date"
                required
              />
            </div>
            {/* Error Message */}
            {error && <p className="text-red-500 text-sm">{error}</p>}
          </div>
          <div className="flex justify-end space-x-2">
            {/* Submit Button */}
            <Button
              type="submit"
              className={`px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 focus:outline-none focus:ring focus:ring-blue-500 ${
                loading ? 'opacity-50 cursor-not-allowed' : ''
              }`}
              disabled={loading}
            >
              {loading ? 'Sending...' : 'Book Now'}
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
