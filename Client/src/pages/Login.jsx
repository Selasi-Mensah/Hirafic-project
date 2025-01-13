
import React, { useState, useEffect } from 'react';
import { AlertCircle } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    remember: false,
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // useEffect(() => {
  //   if (sessionStorage.getItem('access_token')) {
  //     const username = sessionStorage.getItem('username');
  //     if (sessionStorage.getItem('role') === 'Artisan') {
  //       navigate(`/artisan/${username}`);
  //     }
  //     else {
  //       navigate(`/client/${username}`);
  //     }
  //   }
  // }, [navigate]);

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

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">Welcome Back</CardTitle>
          <CardDescription className="text-center">
            Login to your account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
            
            <div className="space-y-2">
              <label htmlFor="email" className="block text-sm font-medium">
                Email Address
              </label>
              <Input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter your email"
                className="w-full"
                required
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="block text-sm font-medium">
                Password
              </label>
              <Input
                id="password"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
                className="w-full"
                required
              />
            </div>

            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={formData.remember}
                  onChange={handleCheckboxChange}
                  className="rounded border-gray-300" />
                <span className="ml-2">Remember me</span>
              </label>
              <a href="/forgot-password" className="text-blue-600 hover:text-blue-800">
                Forgot Password?
              </a>
            </div>

            <Button
              type="submit"
              className="w-full"
              disabled={loading}
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </Button>

            <p className="text-center text-sm">
              Don't have an account?{' '}
              <a href="/register" className="text-blue-600 hover:text-blue-800">
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
