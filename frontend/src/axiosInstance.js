import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'https://docpedia.onrender.com', // Backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
