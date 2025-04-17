import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

// Create an axios instance with configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
  withCredentials: true,  // Ensures cookies (access & refresh tokens) are sent with every request
});

// Response Interceptor: Handle 401 errors by attempting to refresh the access token
apiClient.interceptors.response.use(
  (response) => response.data,
  async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry && originalRequest.url !== "/refresh"
    ) {
      originalRequest._retry = true;
      try {
        const refreshResponse = await apiClient.post("/refresh");
        return apiClient(originalRequest);
      } catch (refreshError) {
        // If the refresh request fails, reject the promise.
        localStorage.setItem("reloadFlag", "0");
        console.error("Interceptor error:", error.response?.data || error.message);
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
