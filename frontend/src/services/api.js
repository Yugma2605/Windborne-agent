import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.data);
    return response;
  },
  (error) => {
    console.error('API Error Details:', {
      message: error.message,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      config: {
        url: error.config?.url,
        method: error.config?.method,
        headers: error.config?.headers
      }
    });
    return Promise.reject(error);
  }
);

export const balloonAPI = {
  // Ask the agent a question
  askQuestion: async (question) => {
    try {
      const response = await api.post('/ask', { question });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get response from agent');
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('Backend is not available');
    }
  },

  // Get balloons data
  get: async (url) => {
    try {
      const response = await api.get(url);
      return response;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch data');
    }
  }
};

export default api;
