import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';
// Import shadcn/ui components
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

/**
 * LoginForm Component
 * A dark-themed login form component with email and password fields,
 * error handling, and loading states.
 * 
 * Features:
 * - Email and password validation
 * - Loading state during form submission
 * - Error message display
 * - Remember me checkbox
 * - Forgot password link
 * - Sign up link for new users
 */
const LoginForm = () => {
  // State management for form data, error messages, and loading state
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  /**
   * Handles input field changes
   * Updates form data and clears any existing error messages
   * @param {Event} e - The input change event
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError(''); // Clear error when user starts typing
  };

  /**
   * Handles form submission
   * Validates inputs and simulates an API call
   * @param {Event} e - The form submission event
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Basic form validation
    if (!formData.email || !formData.password) {
      setError('Please fill in all fields');
      setLoading(false);
      return;
    }

    try {
      // Simulate API call with 1 second delay
      // Replace this with your actual API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      console.log('Login successful', formData);
      
    } catch (err) {
      setError('Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

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

export default LoginForm;