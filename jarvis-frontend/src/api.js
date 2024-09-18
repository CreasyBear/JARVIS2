import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

export const queryAPI = async (query) => {
  try {
    const response = await axios.post(`${API_URL}/query`, { query });
    return response.data;
  } catch (error) {
    console.error('Error querying API:', error);
    throw error;
  }
};

export const executeTask = async (task) => {
  try {
    const response = await axios.post(`${API_URL}/execute`, task);
    return response.data;
  } catch (error) {
    console.error('Error executing task:', error);
    throw error;
  }
};