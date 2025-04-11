import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/api.js';
import { useAuth } from "../context/AuthProvider";




function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { setUser } = useAuth();

    const navigate = useNavigate();

    const validateForm = () => {
        if (!username || !password) {
            setError('Username and password are required');
            return false;
        }
        setError('');
        return true;
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!validateForm()) return;
        setLoading(true);

        try {
            const response = await apiClient.post('/login', {username, password } );
            const userData = await apiClient.get('/users/me');
            setUser(userData);
            setLoading(false);
            navigate('/dashboard');  // Redirect after login
        } catch (error) {
            setLoading(false);
            setError(error.response?.data?.detail || 'Authentication failed!');
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <br></br><br></br>
                <button>
                    <a href='/register'>Register Here</a>
                </button>
                <br></br><br></br>
                <button type="submit" disabled={loading}>
                    {loading ? 'Logging in...' : 'Login'}
                </button>
                {error && <p style={{ color: 'red' }}>{error}</p>}
            </form>
        </div>
    );
}

export default Login;
