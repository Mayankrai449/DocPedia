import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://127.1.1.1:8001', // Backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
