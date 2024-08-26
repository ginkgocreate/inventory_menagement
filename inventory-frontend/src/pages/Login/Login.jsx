import React from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate('/test');
  };

  return (
    <div>
      <h1>Login Component</h1>
      <button onClick={handleButtonClick}>Go to Test</button>
    </div>
  );
};

export default Login;
