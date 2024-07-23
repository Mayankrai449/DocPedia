import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8002', // Backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
