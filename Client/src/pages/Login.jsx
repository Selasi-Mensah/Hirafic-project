import React, { useState, useEffect } from 'react';
import { AlertCircle } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
// import { Link } from "react-router-dom";
import Client from "./Client";
import Artisan from "./Artisan";


const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    remember: false,
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // if user is already logged in, redirect to their dashboard
  useEffect(() => {
    if (sessionStorage.getItem('access_token')) {
      const username = sessionStorage.getItem('username');
      if (sessionStorage.getItem('role') === 'Artisan') {
        navigate(`/artisan/${username}`);
        // window.location.href = `/artisan/${username}`;
      }
      else {
        navigate(`/client/${username}`);
        // window.location.href = `/client/${username}`;
      }
    } else {
      setLoading(false);
    }
  }, [navigate]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError(''); // Clear error when user starts typing
  };

  const handleCheckboxChange = (e) => {
    setFormData({
      ...formData,
      remember: e.target.checked,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Basic validation
    if (!formData.email || !formData.password) {
      setError('Please fill in all fields');
      setLoading(false);
      return;
    }

    try {
      // Calling backend API to login
      console.log(formData);
      const response = await axios.post('http://127.0.0.1:5000/login', formData);
      // console.log(response.data['access_token']);
      sessionStorage.setItem('access_token', response.data.access_token);
      sessionStorage.setItem('username', response.data.user.username);
      sessionStorage.setItem('role', response.data.user.role);
      const username = response.data.user.username;
      console.log(response.data.user.username);
      if (response.data.user.role === 'Artisan') {
        navigate(`/artisan/${username}`);
      } else if (response.data.user.role === 'Client') {
        navigate(`/client/${username}`);
      } else {
        navigate('/')
      }
      // Handle successful login here
      console.log('Login successful', formData);
      return; 
    } catch (err) {
      console.log(err)
      if (err.response && err.response.status === 400) {
          setError('Invalid email or password'); 
      } else {
        setError('Unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return;
  }

  return (
    // Main container with dark theme background
    <div className="flex items-center justify-center min-h-screen bg-gray-900">
      {/* Login card with dark theme styling */}
      <Card className="w-full max-w-md bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center text-white">Welcome Back</CardTitle>
          <CardDescription className="text-center text-gray-400">
            Login to your Hirafic account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Error alert display */}
            {error && (
              <Alert variant="destructive" className="border-red-800 bg-red-900/50">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
            
            {/* Email input field */}
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
                className="w-full bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:border-blue-500"
                required
              />
            </div>

            {/* Password input field */}
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
                placeholder="Enter your password"
                className="w-full bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:border-blue-500"
                required
              />
            </div>

            {/* Remember me checkbox and Forgot password link */}
            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center text-gray-300">
                <input type="checkbox" className="rounded border-gray-600 bg-gray-700" />
                <span className="ml-2">Remember me</span>
              </label>
              <a href="/forgot-password" className="text-blue-400 hover:text-blue-300">
                Forgot Password?
              </a>
            </div>

            {/* Submit button with loading state */}
            <Button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700"
              disabled={loading}
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </Button>

            {/* Sign up link for new users */}
            <p className="text-center text-sm text-gray-400">
              Don't have an account?{' '}
              <a href="/register" className="text-blue-400 hover:text-blue-300">
                Sign up
              </a>
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default Login;