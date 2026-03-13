import { useState } from 'react';
import { Bell, CheckCircle } from 'lucide-react';
import { subscribe } from '../api';

export default function SubscribeForm() {
  const [form, setForm] = useState({
    email: '',
    name: '',
    origin_keywords: '',
    destination_keywords: '',
    frequency: 'daily',
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await subscribe(form);
      setSuccess(true);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al suscribirse.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="glass-card p-8 text-center">
        <CheckCircle className="w-12 h-12 text-green-400 mx-auto mb-3" />
        <h3 className="text-lg font-bold text-white mb-1">¡Suscripción activa!</h3>
        <p className="text-gray-400 text-sm">Te avisaremos cuando haya empty legs que coincidan con tus criterios.</p>
      </div>
    );
  }

  return (
    <div className="glass-card p-6 sm:p-8">
      <div className="flex items-center gap-3 mb-6">
        <Bell className="w-6 h-6 text-purple-400" />
        <div>
          <h3 className="text-lg font-bold text-white">Alertas de Empty Legs</h3>
          <p className="text-gray-400 text-sm">Recibí notificaciones cuando haya vuelos que te interesen.</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <input
            type="text"
            placeholder="Tu nombre"
            className="input-field"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
          <input
            type="email"
            placeholder="Tu email *"
            required
            className="input-field"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <input
            type="text"
            placeholder="Origen (ej: Buenos Aires, Miami)"
            className="input-field"
            value={form.origin_keywords}
            onChange={(e) => setForm({ ...form, origin_keywords: e.target.value })}
          />
          <input
            type="text"
            placeholder="Destino (ej: Punta Cana, London)"
            className="input-field"
            value={form.destination_keywords}
            onChange={(e) => setForm({ ...form, destination_keywords: e.target.value })}
          />
        </div>
        <div className="flex items-center gap-3">
          <select
            className="input-field flex-1"
            value={form.frequency}
            onChange={(e) => setForm({ ...form, frequency: e.target.value })}
          >
            <option value="immediate">Inmediata</option>
            <option value="daily">Resumen diario</option>
            <option value="weekly">Resumen semanal</option>
          </select>
          <button
            type="submit"
            disabled={loading}
            className="btn-primary whitespace-nowrap disabled:opacity-50"
          >
            {loading ? 'Suscribiendo...' : 'Suscribirme'}
          </button>
        </div>

        {error && <p className="text-red-400 text-sm">{error}</p>}
      </form>
    </div>
  );
}
