import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { registerUser } from '../services/user';

// Mesma paleta de cores moderna (Dark Mode)
const theme = {
  background: '#121214',
  card: '#202024',
  text: '#E1E1E6',
  textMuted: '#A8A8B3',
  border: '#323238',
  primary: '#00875F', 
  danger: '#F75A68',
  inputBg: '#121214',
};

export function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e: FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      await registerUser({ name, email, password });
      alert('Conta criada com sucesso! Faça seu login.');
      navigate('/login');
    } catch (err: any) {
      console.error(err);
      const errorMessage = err.response?.data?.detail || 'Erro ao criar conta. Verifique os dados.';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: theme.background, color: theme.text, fontFamily: 'system-ui, sans-serif', padding: '1rem' }}>
      
      <div style={{ width: '100%', maxWidth: '400px', padding: '2.5rem', backgroundColor: theme.card, borderRadius: '12px', border: `1px solid ${theme.border}`, boxShadow: '0 4px 6px rgba(0,0,0,0.2)' }}>
        
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h2 style={{ margin: 0, fontSize: '1.75rem', color: theme.text }}>Criar Conta</h2>
          <p style={{ color: theme.textMuted, marginTop: '0.5rem', fontSize: '0.875rem' }}>Junte-se ao Tracko hoje mesmo</p>
        </div>

        {error && (
          <div style={{ padding: '0.75rem', marginBottom: '1.5rem', backgroundColor: 'rgba(247, 90, 104, 0.1)', border: `1px solid ${theme.danger}`, borderRadius: '8px', color: theme.danger, textAlign: 'center', fontSize: '0.875rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <input 
            type="text" 
            placeholder="Seu Nome" 
            value={name} 
            onChange={(e) => setName(e.target.value)} 
            required 
            style={{ padding: '1rem', borderRadius: '8px', border: `1px solid ${theme.border}`, backgroundColor: theme.inputBg, color: theme.text, fontSize: '1rem', outline: 'none' }}
          />
          <input 
            type="email" 
            placeholder="Seu E-mail" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
            style={{ padding: '1rem', borderRadius: '8px', border: `1px solid ${theme.border}`, backgroundColor: theme.inputBg, color: theme.text, fontSize: '1rem', outline: 'none' }}
          />
          <input 
            type="password" 
            placeholder="Crie uma Senha" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
            minLength={6}
            style={{ padding: '1rem', borderRadius: '8px', border: `1px solid ${theme.border}`, backgroundColor: theme.inputBg, color: theme.text, fontSize: '1rem', outline: 'none' }}
          />
          <button 
            type="submit" 
            disabled={isLoading}
            style={{ padding: '1rem', cursor: isLoading ? 'not-allowed' : 'pointer', backgroundColor: theme.primary, color: 'white', border: 'none', borderRadius: '8px', fontSize: '1rem', fontWeight: 'bold', marginTop: '0.5rem', opacity: isLoading ? 0.7 : 1, transition: 'opacity 0.2s' }}
          >
            {isLoading ? 'Cadastrando...' : 'Cadastrar'}
          </button>
        </form>

        <p style={{ marginTop: '2rem', textAlign: 'center', color: theme.textMuted, fontSize: '0.875rem' }}>
          Já tem uma conta? <Link to="/login" style={{ color: theme.primary, textDecoration: 'none', fontWeight: 'bold' }}>Faça Login aqui</Link>
        </p>

      </div>
    </div>
  );
}