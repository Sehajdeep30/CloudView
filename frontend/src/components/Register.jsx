import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/api.js';
import { useAuth } from "../context/AuthProvider";


function Register() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { setUser } = useAuth();

    const navigate = useNavigate();

    const validateForm = () => {
        if (!username || !password || !email || !password2) {
            setError('All fields are required');
            return false;
        } if (password !== password2) {
            setError('Passwords do not match');
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
            console.log("Registering user:", username, email);
            const response = await apiClient.post('/registration', { username, password, password2, email });
            console.log("registered");
            setLoading(false);
            navigate('/login');  // Redirect after registeration
        } catch (error) {
            setLoading(false);
            setError(error.response?.data?.detail[0].msg?"Enter a valid email address": 'Registration failed!');
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
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
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

                <div>
                    <label>Confirm Password:</label>
                    <input
                        type="password"
                        value={password2}
                        onChange={(e) => setPassword2(e.target.value)}
                    />
                </div>
                <br></br><br></br>
                <button>
                    <a href='/login'>Already have an account? Login Here</a>
                </button>
                <br></br><br></br>
                <button type="submit" disabled={loading}>
                    {loading ? 'Creating New User...' : 'Register'}
                </button>
                {error && <p style={{ color: 'red' }}>{error}</p>}
            </form>
        </div>
    );
}

export default Register;
