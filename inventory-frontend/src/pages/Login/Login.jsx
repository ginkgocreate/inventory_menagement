import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { postData } from 'utils/api';

const Login = () => {
    const [loginId, setLoginId] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleLogin = (event) => {
        event.preventDefault();
        postData('/auth/login', { login_id: loginId, password: password })
        .then(data => {
            if (data.message === 'Login successful!') {
                navigate('/menu');
            } else {
                setMessage(data.message);
            }
        });
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <label>Username:</label><br />
                <input 
                    type="text" 
                    value={loginId} 
                    onChange={(e) => setLoginId(e.target.value)} 
                /><br />
                <label>Password:</label><br />
                <input 
                    type="password" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)} 
                /><br /><br />
                <button type="submit">Login</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Login;
