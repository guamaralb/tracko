import { useEffect, useState } from 'react';
import type { SubmitEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';
import { createTask, deleteTask, updateTaskStatus } from '../services/task';

interface User {
  id: string;
  email: string;
  name: string;
}

interface Task {
  id: string;
  title: string;
  description: string | null;
  status: string;
  start_date: string | null;
  end_date: string | null;
  user_id_creator: string; // <-- Adicione esta linha
}

interface TaskResponse {
  tasks: Task[];
  total: number;
  offset: number;
  limit: number;
}

// Paleta de cores moderna (Dark Mode)
const theme = {
  background: '#121214',
  card: '#202024',
  text: '#E1E1E6',
  textMuted: '#A8A8B3',
  border: '#323238',
  primary: '#00875F', // Um verde moderno, mude para '#007BFF' se preferir o azul
  danger: '#F75A68',
  inputBg: '#121214',
};

export function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  
  const [newTitle, setNewTitle] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [userResponse, tasksResponse] = await Promise.all([
          api.get('/users/me'),
          api.get('/tasks/')
        ]);
        
        const currentUser = userResponse.data;
        setUser(currentUser);
        
        const taskData = tasksResponse.data as TaskResponse;
        const allTasks = taskData.tasks || [];
        
        // FILTRO MÁGICO: Guarda só as tarefas que pertencem ao usuário logado
        const myTasks = allTasks.filter(task => task.user_id_creator === currentUser.id);
        
        setTasks(myTasks);
      } catch (err) {
        console.error("Erro ao buscar dados", err);
        localStorage.removeItem('access_token');
        navigate('/login');
      }
    };

    fetchData();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  const handleCreateTask = async (e: SubmitEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const createdTask = await createTask({ 
        title: newTitle, 
        description: newDescription 
      });

      setTasks((prevTasks) => [createdTask, ...prevTasks]);
      setNewTitle('');
      setNewDescription('');
    } catch (err) {
      console.error("Erro ao criar tarefa:", err);
      alert("Não foi possível criar a tarefa.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!window.confirm("Tem certeza que deseja excluir esta tarefa?")) return;
    
    try {
      await deleteTask(taskId);
      setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
    } catch (err) {
      console.error("Erro ao excluir tarefa:", err);
      alert("Não foi possível excluir a tarefa.");
    }
  };

  const handleStatusChange = async (taskId: string, newStatus: string) => {
    try {
      // 1. Chama a API para atualizar
      await updateTaskStatus(taskId, newStatus);
      
      // 2. Atualiza a lista na tela instantaneamente
      setTasks((prevTasks) => 
        prevTasks.map((task) => 
          task.id === taskId ? { ...task, status: newStatus } : task
        )
      );
    } catch (err) {
      console.error("Erro ao atualizar status:", err);
      alert("Não foi possível atualizar o status da tarefa. Verifique se a rota PATCH existe no backend.");
    }
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: theme.background, color: theme.text, padding: '2rem 1rem', fontFamily: 'system-ui, sans-serif' }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        
        {/* --- HEADER --- */}
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem', borderBottom: `1px solid ${theme.border}`, paddingBottom: '1rem' }}>
          <h1 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold' }}>
            Bem-vindo, <span style={{ color: theme.primary }}>{user?.name || 'Carregando...'}</span>
          </h1>
          <button 
            onClick={handleLogout} 
            style={{ padding: '0.5rem 1.5rem', backgroundColor: 'transparent', color: theme.textMuted, border: `1px solid ${theme.border}`, borderRadius: '6px', cursor: 'pointer', transition: 'all 0.2s' }}
          >
            Sair
          </button>
        </header>

        {/* --- FORMULÁRIO DE NOVA TAREFA --- */}
        <section style={{ marginBottom: '3rem', padding: '2rem', backgroundColor: theme.card, borderRadius: '12px', border: `1px solid ${theme.border}`, boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
          <h2 style={{ marginTop: 0, marginBottom: '1.5rem', fontSize: '1.25rem' }}>Criar Nova Tarefa</h2>
          <form onSubmit={handleCreateTask} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <input 
              type="text" 
              placeholder="Título da tarefa..." 
              value={newTitle} 
              onChange={(e) => setNewTitle(e.target.value)} 
              required 
              style={{ padding: '1rem', borderRadius: '8px', border: `1px solid ${theme.border}`, backgroundColor: theme.inputBg, color: theme.text, fontSize: '1rem', outline: 'none' }}
            />
            <textarea 
              placeholder="Descrição (opcional)..." 
              value={newDescription} 
              onChange={(e) => setNewDescription(e.target.value)} 
              style={{ padding: '1rem', borderRadius: '8px', border: `1px solid ${theme.border}`, backgroundColor: theme.inputBg, color: theme.text, fontSize: '1rem', minHeight: '100px', resize: 'vertical', outline: 'none' }}
            />
            <button 
              type="submit" 
              disabled={isSubmitting}
              style={{ padding: '1rem', cursor: isSubmitting ? 'not-allowed' : 'pointer', backgroundColor: theme.primary, color: 'white', border: 'none', borderRadius: '8px', fontSize: '1rem', fontWeight: 'bold', marginTop: '0.5rem', opacity: isSubmitting ? 0.7 : 1 }}
            >
              {isSubmitting ? 'Salvando...' : 'Adicionar Tarefa'}
            </button>
          </form>
        </section>

        {/* --- LISTA DE TAREFAS --- */}
        <section>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '1.5rem' }}>Minhas Tarefas</h2>
          {tasks.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '3rem', backgroundColor: theme.card, borderRadius: '12px', border: `1px dashed ${theme.border}` }}>
              <p style={{ color: theme.textMuted, margin: 0 }}>Nenhuma tarefa encontrada. Que tal criar uma acima?</p>
            </div>
          ) : (
            <ul style={{ listStyleType: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {tasks.map(task => (
                <li key={task.id} style={{ padding: '1.5rem', borderRadius: '12px', backgroundColor: theme.card, border: `1px solid ${theme.border}`, transition: 'transform 0.2s' }}>
                  <h3 style={{ marginTop: 0, marginBottom: '0.5rem', fontSize: '1.125rem' }}>{task.title}</h3>
                  {task.description && <p style={{ color: theme.textMuted, margin: '0 0 1rem 0', lineHeight: '1.5' }}>{task.description}</p>}
                  
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1.5rem', paddingTop: '1rem', borderTop: `1px solid ${theme.border}` }}>
                    <select 
                    value={task.status}
                    onChange={(e) => handleStatusChange(task.id, e.target.value)}
                    style={{ 
                        padding: '0.25rem 0.75rem', 
                        backgroundColor: theme.inputBg, 
                        color: theme.text, 
                        borderRadius: '6px', 
                        fontSize: '0.875rem', 
                        fontWeight: '500', 
                        border: `1px solid ${theme.border}`,
                        cursor: 'pointer',
                        outline: 'none'
                    }}
                    >
                    <option value="todo">A Fazer</option>
                    <option value="in_progress">Em Progresso</option>
                    <option value="cancelled">Cancelado</option>
                    <option value="done">Concluído</option>
                    </select>
                    
                    <button 
                      onClick={() => handleDeleteTask(task.id)}
                      style={{ padding: '0.5rem 1rem', backgroundColor: 'transparent', color: theme.danger, border: `1px solid ${theme.danger}`, borderRadius: '6px', cursor: 'pointer', fontSize: '0.875rem', fontWeight: 'bold' }}
                    >
                      Excluir
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>

      </div>
    </div>
  );
}