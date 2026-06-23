// src/services/task.ts
import { api } from '../api';

// Baseado no seu backend, o título é obrigatório, e a descrição é opcional.
// O status geralmente assume "TODO" por padrão no backend.
export interface TaskCreateData {
  title: string;
  description?: string;
}

export const createTask = async (taskData: TaskCreateData) => {
  const response = await api.post('/tasks/', taskData);
  return response.data;
};

export const deleteTask = async (taskId: string) => {
  await api.delete(`/tasks/${taskId}`);
};

export const updateTaskStatus = async (taskId: string, newStatus: string) => {
  const response = await api.patch(`/tasks/${taskId}`, { status: newStatus });
  return response.data;
};