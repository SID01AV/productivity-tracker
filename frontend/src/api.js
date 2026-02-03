import axios from "axios";

// For dev in browser we use Vite proxy (`/api` → FastAPI).
// For Capacitor/mobile builds you can override with VITE_API_URL, e.g.:
// VITE_API_URL=http://192.168.1.10:8000 npm run build

const API_BASE_URL = import.meta.env.VITE_API_URL || "";

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;

