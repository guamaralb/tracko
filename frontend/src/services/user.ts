// src/services/user.ts
import { api } from '../api';

// Ajuste os campos conforme o seu UserCreateSchema no backend
export interface UserCreateData {
  name: string;
  email: string;
  password: string;
}

export const registerUser = async (userData: UserCreateData) => {
  const response = await api.post('/users/', userData);
  return response.data;
};