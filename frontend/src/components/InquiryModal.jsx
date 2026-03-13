import { useState } from 'react';
import { X, CheckCircle, ArrowRight } from 'lucide-react';
import { submitInquiry } from '../api';

export default function InquiryModal({ leg, onClose }) {
  const [form, setForm] = useState({
    name: '',
    email: '',
    phone: '',
    passengers: 1,
    message: '',
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await submitInquiry({
        ...form,
        empty_leg: leg.id,
      });
      setSuccess(true);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al enviar la consulta. Intentá de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="glass-card p-6 sm:p-8 w-full max-w-md relative z-10">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-300 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {success ? (
          /* Estado de éxito */
          <div className="text-center py-8">
            <CheckCircle className="w-16 h-16 text-green-400 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-white mb-2">¡Consulta enviada!</h3>
            <p className="text-gray-400 text-sm mb-6">
              Nos pondremos en contacto con vos a la brevedad.
            </p>
            <button onClick={onClose} className="btn-primary">
              Cerrar
            </button>
          </div>
        ) : (
          <>
            {/* Header */}
            <h3 className="text-lg font-bold text-white mb-1">Me interesa este vuelo</h3>
            <div className="flex items-center gap-2 text-purple-400 text-sm mb-6">
              <span>{leg.origin_display}</span>
              <ArrowRight className="w-3.5 h-3.5" />
              <span>{leg.destination_display}</span>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <input
                  type="text"
                  placeholder="Nombre *"
                  required
                  className="input-field"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
              </div>
              <div>
                <input
                  type="email"
                  placeholder="Email *"
                  required
                  className="input-field"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                />
              </div>
              <div>
                <input
                  type="tel"
                  placeholder="Teléfono (opcional)"
                  className="input-field"
                  value={form.phone}
                  onChange={(e) => setForm({ ...form, phone: e.target.value })}
                />
              </div>
              <div>
                <input
                  type="number"
                  placeholder="Pasajeros"
                  min={1}
                  max={leg.max_passengers || 20}
                  className="input-field"
                  value={form.passengers}
                  onChange={(e) => setForm({ ...form, passengers: parseInt(e.target.value) || 1 })}
                />
              </div>
              <div>
                <textarea
                  placeholder="Mensaje (opcional)"
                  rows={3}
                  className="input-field resize-none"
                  value={form.message}
                  onChange={(e) => setForm({ ...form, message: e.target.value })}
                />
              </div>

              {error && (
                <p className="text-red-400 text-sm">{error}</p>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full btn-primary disabled:opacity-50"
              >
                {loading ? 'Enviando...' : 'Enviar consulta'}
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}
