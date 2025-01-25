import React, { useState, useEffect} from 'react';
import { AlertCircle } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Registration = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirm_password: '',
    phone_number: '',
    location: '',
    role: '',
  });

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (sessionStorage.getItem('access_token')) {
      const username = sessionStorage.getItem('username');
      if (sessionStorage.getItem('role') === 'Artisan') {
        navigate(`/artisan/${username}`);
      }
      else {
        navigate(`/client/${username}`);
      }
    }
  }, [navigate]);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError('');
  };

  const handleSelectChange = (value) => {
    setFormData(prev => ({
      ...prev,
      role: value
    }));
    setError('');
  };

  const validateForm = () => {
    if (!formData.username || !formData.email || 
        !formData.phone_number || !formData.location || !formData.password || !formData.confirm_password || 
        !formData.role) {
      setError('Please fill in all fields');
      return false;
    }

    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match');
      return false;
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError('Please enter a valid email address');
      return false;
    }

    const phoneRegex = /^\+?[\d\s-]{10,}$/;
    if (!phoneRegex.test(formData.phone_number)) {
      setError('Please enter a valid phone number');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    try {
      await axios.post('http://127.0.0.1:5000/register', formData)
      console.log('Registration successful');
      navigate('/login');
    } catch (err) {
      console.log(err)
      if (err.response && err.response.status === 400) {
        if (err.response.data.error.username) {
          setError("The username you entered is already taken. Please choose a different username.");
        }
        else {
          setError("The email address you entered is already registered. Please use a different email address or log in.");
        }
      } else {
        console.error('Registration failed', err);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900 py-8">
      <Card className="w-full max-w-lg mx-4 bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center text-white">Create Account</CardTitle>
          <CardDescription className="text-center text-gray-400">
            Join our community today
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <Alert variant="destructive" className="border-red-800 bg-red-900/50">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-2">
              <label htmlFor="username" className="block text-sm font-medium text-gray-200">
                User Name
              </label>
              <Input
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="Enter your user name" 
                className="bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:border-blue-500"
                required
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="email" className="block text-sm font-medium text-gray-200">
                Email Address
              </label>
              <Input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter your email"
                className="bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:border-blue-500"
                required
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="phone" className="block text-sm font-medium text-gray-200">
                Phone Number
              </label>
              <Input
                id="phone_number"
                name="phone_number"
                type="tel"
                value={formData.phone_number}
                onChange={handleChange}
                placeholder="Enter your phone number"
                className="bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:border-blue-500"
                required
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="Location" className="block text-sm font-medium text-gray-200">
                Location Address
              </label>
              <Input
                id="location"
                name="location"
                type="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="country, city, state, postal code"
                className="bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:border-blue-500"
                required
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="role" className="block text-sm font-medium text-gray-200">
                Role
              </label>
              <Select value={formData.role} onValueChange={handleSelectChange}>
                <SelectTrigger className="bg-gray-700 border-gray-600 text-gray-200">
                  <SelectValue placeholder="Select role" />
                </SelectTrigger>
                <SelectContent className="bg-gray-800 border-gray-700">
                  <SelectItem value="Artisan" className="text-gray-200 hover:bg-gray-700">Artisan</SelectItem>
                  <SelectItem value="Client" className="text-gray-200 hover:bg-gray-700">Client</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="block text-sm font-medium text-gray-200">
                Password
              </label>
              <Input
                id="password"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Create a password"
                className="bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:border-blue-500"
                required
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-200">
                Confirm Password
              </label>
              <Input
                id="confirm_password"
                name="confirm_password"
                type="password"
                value={formData.confirm_password}
                onChange={handleChange}
                placeholder="Confirm your password"
                className="bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:border-blue-500"
                required
              />
            </div>

            <Button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700"
              disabled={loading}
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </Button>

            <p className="text-center text-sm text-gray-400">
              Already have an account?{' '}
              <a href="/login" className="text-blue-400 hover:text-blue-300">
                Sign in
              </a>
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default Registration;