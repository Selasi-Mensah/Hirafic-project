import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogClose } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import axios from 'axios';

const BookModal = ({ artisan, isOpen, onClose }) => {
  const [details, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://127.0.0.1:5000/book', {
        artisan_email: artisan.email,
        client_email: sessionStorage.getItem('email'),
        details,
      }, {
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
        },
      });
      alert('Message sent successfully');
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Book {artisan.username}</DialogTitle>
          <DialogDescription>
            Write booking details for {artisan.username} artisan.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="space-y-4">
            <textarea
              className="w-full p-2 bg-gray-800 text-gray-100 rounded"
              rows="5"
              placeholder="Booking details"
              value={details}
              onChange={(e) => setMessage(e.target.value)}
              required
            />
            {error && <p className="text-red-400">{error}</p>}
            <div className="flex justify-end">
              <Button type="submit" className="bg-blue-600 hover:bg-blue-700" disabled={loading}>
                {loading ? 'Sending...' : 'Book Now'}
              </Button>
            </div>
          </div>
        </form>
        <DialogClose asChild>
          <Button variant="outline" className="mt-4">Close</Button>
        </DialogClose>
      </DialogContent>
    </Dialog>
  );
};

export default BookModal;