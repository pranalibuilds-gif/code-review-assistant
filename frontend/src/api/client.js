import axios from 'axios';
import toast from 'react-hot-toast';

const client = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request Interceptor: Attach JWT and Request ID
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  // Attach a unique Request ID for tracing if not provided
  if (!config.headers['X-Request-ID']) {
    config.headers['X-Request-ID'] = Math.random().toString(36).substring(2, 11);
  }

  return config;
});

// Response Interceptor: Centralized Error Handling
client.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.error?.message || error.message || 'An unexpected error occurred';

    // Handle 401 Unauthorized (Session Expired)
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      if (!window.location.pathname.includes('/login')) {
        toast.error('Session expired. Please login again.');
        window.location.href = '/login';
      }
    } else if (error.response?.status === 403) {
      toast.error("You don't have permission to perform this action.");
    } else {
      toast.error(message);
    }

    return Promise.reject(error);
  }
);

export default client;
