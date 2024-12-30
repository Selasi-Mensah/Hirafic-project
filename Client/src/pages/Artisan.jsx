// ArtisanLogin.jsx
/*import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './ArtisanLogin.css';

const ArtisanLogin = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        rememberMe: false
    });
    const [errors, setErrors] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const validateForm = () => {
        let tempErrors = {};
        if (!formData.email) {
            tempErrors.email = 'Email is required';
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            tempErrors.email = 'Email is invalid';
        }
        if (!formData.password) {
            tempErrors.password = 'Password is required';
        }
        setErrors(tempErrors);
        return Object.keys(tempErrors).length === 0;
    };

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prevData => ({
            ...prevData,
            [name]: type === 'checkbox' ? checked : value
        }));
        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (validateForm()) {
            setIsLoading(true);
            try {
                // API call would go here
                await new Promise(resolve => setTimeout(resolve, 1000)); // Simulated API call
                navigate('/artisan/dashboard');
            } catch (error) {
                setErrors({
                    submit: 'Invalid credentials. Please try again.'
                });
            } finally {
                setIsLoading(false);
            }
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <div className="login-header">
                    <h2>Welcome Back, Artisan!</h2>
                    <p>Please log in to access your profile</p>
                </div>

                {errors.submit && (
                    <div className="error-message">
                        {errors.submit}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="login-form">
                    <div className="form-group">
                        <label htmlFor="email">Email Address</label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            className={`form-input ${errors.email ? 'error' : ''}`}
                            value={formData.email}
                            onChange={handleChange}
                            placeholder="Enter your email"
                        />
                        {errors.email && <span className="error-text">{errors.email}</span>}
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            className={`form-input ${errors.password ? 'error' : ''}`}
                            value={formData.password}
                            onChange={handleChange}
                            placeholder="Enter your password"
                        />
                        {errors.password && <span className="error-text">{errors.password}</span>}
                    </div>

                    <div className="form-options">
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                name="rememberMe"
                                checked={formData.rememberMe}
                                onChange={handleChange}
                            />
                            Remember me
                        </label>
                        <Link to="/forgot-password" className="forgot-password">
                            Forgot Password?
                        </Link>
                    </div>

                    <button 
                        type="submit" 
                        className={`login-button ${isLoading ? 'loading' : ''}`}
                        disabled={isLoading}
                    >
                        {isLoading ? 'Logging in...' : 'Login'}
                    </button>
                </form>

                <div className="login-footer">
                    <p>Don't have an account?</p>
                    <Link to="/artisan/signup" className="signup-link">
                        Sign up now
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default ArtisanLogin;
*/