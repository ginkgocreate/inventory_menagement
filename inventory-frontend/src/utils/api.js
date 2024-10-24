import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

export const postData = async (endpoint, data) => {
    try {
        const response = await axios.post(`${API_BASE_URL}${endpoint}`, data, { withCredentials: true });
        return response.data;
    } catch (error) {
        console.error(`Error with POST request to ${endpoint}:`, error);
        throw error;
    }
};

export const getData = async (endpoint, params = {}) => {
    try {
        const response = await axios.get(`${API_BASE_URL}${endpoint}`, { 
            params,
            withCredentials: true
            });
        return response.data;
    } catch (error) {
        console.error(`Error with GET request to ${endpoint}:`, error);
        throw error;
    }
};
