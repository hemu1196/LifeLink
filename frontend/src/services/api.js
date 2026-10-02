import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Attach JWT Bearer Token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('lifelink_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authAPI = {
  login: (data) => api.post('/api/auth/login', data),
  register: (data) => api.post('/api/auth/register', data),
  getMe: () => api.get('/api/auth/me'),
};

export const emergencyBoardAPI = {
  getBoard: (priority) => api.get('/api/emergency-board/', { params: { priority } }),
};

export const donorAPI = {
  getProfile: () => api.get('/api/donor/profile'),
  updateProfile: (data) => api.put('/api/donor/profile', data),
  respond: (requestId) => api.post(`/api/donor/respond/${requestId}`),
  getResponses: () => api.get('/api/donor/responses'),
  getDonations: () => api.get('/api/donor/donations'),
  getEligibility: () => api.get('/api/donor/eligibility'),
};

export const hospitalAPI = {
  getDashboard: () => api.get('/api/hospital/dashboard'),
  createRequest: (data) => api.post('/api/hospital/requests', data),
  getRequests: () => api.get('/api/hospital/requests'),
  updateRequestStatus: (id, status) => api.put(`/api/hospital/requests/${id}/status`, null, { params: { status_str: status } }),
  getDonorResponses: () => api.get('/api/hospital/responses'),
  updateResponseStatus: (id, status) => api.put(`/api/hospital/responses/${id}/status`, { status }),
};

export const bloodBankAPI = {
  getSummary: () => api.get('/api/blood-bank/summary'),
  getInventory: () => api.get('/api/blood-bank/inventory'),
  addInventory: (data) => api.post('/api/blood-bank/add', data),
};

export const adminAPI = {
  getStats: () => api.get('/api/admin/stats'),
  getHospitals: () => api.get('/api/admin/hospitals'),
  verifyHospital: (id, status) => api.put(`/api/admin/hospitals/${id}/verify`, null, { params: { status_str: status } }),
  getDonors: () => api.get('/api/admin/donors'),
  getBloodBanks: () => api.get('/api/admin/blood-banks'),
};

export const matchingAPI = {
  findDonors: (bloodGroup, city, area) => api.get('/api/matching/find-donors', { params: { blood_group: bloodGroup, city, area } }),
  checkStock: (bloodGroup) => api.get('/api/matching/stock-check', { params: { blood_group: bloodGroup } }),
};

export const analyticsAPI = {
  getSummary: () => api.get('/api/analytics/summary'),
};

export const notificationsAPI = {
  getNotifications: () => api.get('/api/notifications/'),
  markAsRead: (id) => api.put(`/api/notifications/${id}/read`),
};

export default api;
