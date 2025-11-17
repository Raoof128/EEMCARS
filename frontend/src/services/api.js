import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth Service
export const authService = {
  login: async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const response = await api.post('/auth/token', formData);
    return response.data;
  },
  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Dashboard Service
export const dashboardService = {
  getSummary: async () => {
    const response = await api.get('/dashboard/summary');
    return response.data;
  },
  getMaturityHeatmap: async () => {
    const response = await api.get('/dashboard/maturity-heatmap');
    return response.data;
  },
  getTrends: async (days = 30) => {
    const response = await api.get(`/dashboard/trends?days=${days}`);
    return response.data;
  },
};

// Controls Service
export const controlsService = {
  getAll: async () => {
    const response = await api.get('/controls/');
    return response.data;
  },
  getById: async (controlId) => {
    const response = await api.get(`/controls/${controlId}`);
    return response.data;
  },
  scoreControl: async (controlId, assetId) => {
    const response = await api.post(`/controls/${controlId}/score`, { asset_id: assetId });
    return response.data;
  },
  getPillarsSummary: async () => {
    const response = await api.get('/controls/pillars/summary');
    return response.data;
  },
};

// Evidence Service
export const evidenceService = {
  getAll: async (assetId = null, controlId = null) => {
    const params = {};
    if (assetId) params.asset_id = assetId;
    if (controlId) params.control_id = controlId;
    const response = await api.get('/evidence/', { params });
    return response.data;
  },
  create: async (evidenceData) => {
    const response = await api.post('/evidence/', evidenceData);
    return response.data;
  },
};

// Assessment Service
export const assessmentService = {
  getAll: async (limit = 20) => {
    const response = await api.get(`/assessments/?limit=${limit}`);
    return response.data;
  },
  getById: async (runId) => {
    const response = await api.get(`/assessments/${runId}`);
    return response.data;
  },
  triggerAssessment: async (assessmentData) => {
    const response = await api.post('/assessments/run', assessmentData);
    return response.data;
  },
};

// Remediation Service
export const remediationService = {
  getTasks: async (status = null) => {
    const params = status ? { status } : {};
    const response = await api.get('/remediation/tasks', { params });
    return response.data;
  },
  createTask: async (taskData) => {
    const response = await api.post('/remediation/tasks', taskData);
    return response.data;
  },
  executeTask: async (taskId) => {
    const response = await api.post(`/remediation/tasks/${taskId}/execute`);
    return response.data;
  },
  generateTasks: async (controlId) => {
    const response = await api.post('/remediation/generate', { control_id: controlId });
    return response.data;
  },
};

// Reports Service
export const reportsService = {
  generate: async (reportData) => {
    const response = await api.post('/reports/exec', reportData);
    return response.data;
  },
  getById: async (reportId) => {
    const response = await api.get(`/reports/${reportId}`);
    return response.data;
  },
  download: async (reportId) => {
    const response = await api.get(`/reports/${reportId}/download`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

// Agents Service
export const agentsService = {
  getAll: async (status = null) => {
    const params = status ? { status } : {};
    const response = await api.get('/agents/', { params });
    return response.data;
  },
  register: async (agentData) => {
    const response = await api.post('/agents/register', agentData);
    return response.data;
  },
  sendHeartbeat: async (agentId) => {
    const response = await api.post('/agents/heartbeat', { agent_id: agentId, status: 'Active' });
    return response.data;
  },
};

export default api;
