import axios from 'axios';

const api = axios.create({
  baseURL: '/api/flights',
  headers: { 'Content-Type': 'application/json' },
});

const notifApi = axios.create({
  baseURL: '/api/notifications',
  headers: { 'Content-Type': 'application/json' },
});

// Helper: crea instancia autenticada
const authApi = (token) => {
  return axios.create({
    baseURL: '/api/flights',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Token ${token}`,
    },
  });
};

// --- Públicas ---
export const fetchPublicEmptyLegs = (search = '') =>
  api.get(`/public/empty-legs/${search ? `?search=${encodeURIComponent(search)}` : ''}`);

export const submitInquiry = (data) =>
  api.post('/public/inquiries/', data);

// --- Panel Auth ---
export const panelLogin = (password) =>
  api.post('/panel/login/', { password });

export const panelLogout = (token) =>
  authApi(token).post('/panel/logout/');

export const panelCheck = (token) =>
  authApi(token).get('/panel/check/');

// --- Panel ---
export const fetchInquiries = (token, status = '') =>
  authApi(token).get(`/panel/inquiries/${status ? `?status=${status}` : ''}`);

export const updateInquiry = (id, updates, token) =>
  authApi(token).patch(`/panel/inquiries/${id}/`, updates);

export const toggleEmptyLeg = (id, field, token) =>
  authApi(token).patch(`/panel/empty-legs/${id}/toggle/`, { field });

export const fetchEmptyLegs = (params, token) =>
  authApi(token).get('/empty-legs/', { params });

export const fetchDashboardStats = (token) =>
  authApi(token).get('/dashboard/');

// --- Fuentes ---
export const fetchSources = (token) =>
  authApi(token).get('/sources/');

export const triggerScrape = (sourceId, token) =>
  authApi(token).post(`/sources/${sourceId}/trigger-scrape/`);

// --- Otros ---
export const fetchOperators = (token) =>
  authApi(token).get('/operators/');

export const fetchAirports = (token) =>
  authApi(token).get('/airports/');

// --- Notificaciones ---
export const subscribe = (data) =>
  notifApi.post('/subscribe/', data);

export const unsubscribe = (email) =>
  notifApi.post('/unsubscribe/', { email });
