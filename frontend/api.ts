import axios, { AxiosInstance, InternalAxiosRequestConfig } from 'axios';

// ✅ Vite env variable (MUST start with VITE_)
const BASE_URL = import.meta.env.VITE_API_BASE_URL as string;

export const api: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Store updated access token
const updateTokens = (accessToken: string) => {
  localStorage.setItem('access_token', accessToken);
};

// Attach access token to every request
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auto-refresh expired access tokens
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        window.location.href = '#/login';
        return Promise.reject(error);
      }

      try {
        const response = await axios.post(
          `${BASE_URL}/v1/auth/refresh`,
          { refresh_token: refreshToken }
        );

        const { access_token } = response.data;
        updateTokens(access_token);

        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
        }

        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '#/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);
