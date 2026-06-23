import { type ReactNode } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { Register } from './pages/Register';

// 1. Criamos um componente "Guarda" que verifica o token na hora exata do acesso
function ProtectedRoute({ children }: { children: ReactNode }) {
  const isAuthenticated = !!localStorage.getItem('access_token');
  
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rota raiz agora joga direto pro dashboard, e o Guarda decide se deixa ou não */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* 2. Envolvemos o Dashboard com o nosso Guarda */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;