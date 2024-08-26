import React, { useState } from 'react';
import axios from 'axios';

function Test() {
  const [response, setResponse] = useState(null);

  const handleApiCall = () => {
    axios.post('http://localhost:5000/login', {
        "login_id": "admin",
        "user_name": "Administrator",
        "password": "Root#008#",
    })
    .then(res => setResponse(res.data))
    .catch(err => setResponse({ error: err.message }));
  };

  return (
    <div>
      <h1>API Call Test</h1>
      <button onClick={handleApiCall}>Call API</button>
      {response && (
        <div>
          <h2>Response:</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default Test;
