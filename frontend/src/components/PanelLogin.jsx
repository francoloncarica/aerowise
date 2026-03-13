import { useState } from 'react';
import { Plane, Lock } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { panelLogin } from '../api';

export default function PanelLogin() {
  const { login } = useAuth();
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await panelLogin(password);
      login(res.data.token);
    } catch {
      setError('Contraseña incorrecta');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen p-4">
      <div className="glass-card p-8 w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Plane className="w-8 h-8 text-purple-400" />
            <span className="text-2xl font-bold text-white">Aerowise</span>
          </div>
          <p className="text-gray-500 text-sm">Panel de administración</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
            <input
              type="password"
              placeholder="Contraseña"
              required
              className="input-field pl-10"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          {error && (
            <p className="text-red-400 text-sm text-center">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary disabled:opacity-50"
          >
            {loading ? 'Verificando...' : 'Entrar al panel'}
          </button>
        </form>
      </div>
    </div>
  );
}
