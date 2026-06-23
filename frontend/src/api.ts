// src/api.ts
import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Ajuste para a URL real da sua API

export const api = axios.create({
  baseURL: API_URL,
});

// Interceptor para adicionar o token JWT em todas as requisições
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});