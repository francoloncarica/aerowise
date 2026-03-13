import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { fetchInquiries, updateInquiry } from '../api';
import {
  ChevronDown, ChevronUp, Mail, Phone,
  Users, MessageSquare, Clock, CheckCircle, XCircle,
} from 'lucide-react';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';

const STATUS_MAP = {
  pending: { label: 'Pendiente', color: 'yellow', icon: Clock },
  contacted: { label: 'Contactado', color: 'blue', icon: CheckCircle },
  closed: { label: 'Cerrado', color: 'gray', icon: XCircle },
};

const TABS = [
  { key: '', label: 'Todas' },
  { key: 'pending', label: 'Pendientes' },
  { key: 'contacted', label: 'Contactados' },
  { key: 'closed', label: 'Cerrados' },
];

export default function PanelInquiries() {
  const { token } = useAuth();
  const [inquiries, setInquiries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [expandedId, setExpandedId] = useState(null);

  const load = async () => {
    setLoading(true);
    try {
      const res = await fetchInquiries(token, filter);
      setInquiries(res.data);
    } catch {
      setInquiries([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [filter, token]);

  const handleStatusChange = async (id, newStatus) => {
    try {
      const res = await updateInquiry(id, { status: newStatus }, token);
      setInquiries((prev) =>
        prev.map((inq) => (inq.id === id ? res.data : inq))
      );
    } catch {
      // Ignorar
    }
  };

  const handleNoteSave = async (id, notes) => {
    try {
      await updateInquiry(id, { admin_notes: notes }, token);
    } catch {
      // Ignorar
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-6">Consultas</h1>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {TABS.map(({ key, label }) => (
          <button
            key={key}
            onClick={() => setFilter(key)}
            className={`px-4 py-2 rounded-xl text-sm transition-colors ${
              filter === key
                ? 'bg-purple-600/20 text-purple-400 border border-purple-500/30'
                : 'bg-white/5 text-gray-400 border border-white/5 hover:bg-white/10'
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex justify-center py-20">
          <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : inquiries.length === 0 ? (
        <div className="text-center py-20">
          <MessageSquare className="w-12 h-12 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-500">No hay consultas.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {inquiries.map((inq) => {
            const isExpanded = expandedId === inq.id;
            const statusInfo = STATUS_MAP[inq.status] || STATUS_MAP.pending;

            return (
              <div key={inq.id} className="glass-card overflow-hidden">
                {/* Header */}
                <button
                  onClick={() => setExpandedId(isExpanded ? null : inq.id)}
                  className="w-full flex items-center justify-between p-4 hover:bg-white/5 transition-colors text-left"
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="text-white font-medium text-sm">{inq.name}</span>
                        <span className="text-gray-500 text-xs">{inq.email}</span>
                      </div>
                      <p className="text-gray-500 text-xs mt-0.5 truncate">{inq.empty_leg_display}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 flex-shrink-0 ml-3">
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-full bg-${statusInfo.color}-500/20 text-${statusInfo.color}-400`}
                    >
                      {statusInfo.label}
                    </span>
                    <span className="text-gray-600 text-xs">
                      {format(parseISO(inq.created_at), "d MMM", { locale: es })}
                    </span>
                    {isExpanded ? (
                      <ChevronUp className="w-4 h-4 text-gray-500" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-gray-500" />
                    )}
                  </div>
                </button>

                {/* Expanded */}
                {isExpanded && (
                  <div className="px-4 pb-4 border-t border-white/5 pt-4 space-y-4">
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
                      <div className="flex items-center gap-2">
                        <Mail className="w-4 h-4 text-gray-500" />
                        <a
                          href={`mailto:${inq.email}`}
                          className="text-purple-400 hover:underline"
                        >
                          {inq.email}
                        </a>
                      </div>
                      {inq.phone && (
                        <div className="flex items-center gap-2">
                          <Phone className="w-4 h-4 text-gray-500" />
                          <a
                            href={`tel:${inq.phone}`}
                            className="text-purple-400 hover:underline"
                          >
                            {inq.phone}
                          </a>
                        </div>
                      )}
                      <div className="flex items-center gap-2">
                        <Users className="w-4 h-4 text-gray-500" />
                        <span className="text-gray-300">{inq.passengers} pasajero(s)</span>
                      </div>
                    </div>

                    {inq.message && (
                      <div className="bg-white/5 rounded-xl p-3">
                        <p className="text-gray-400 text-xs font-medium mb-1">Mensaje:</p>
                        <p className="text-gray-300 text-sm">{inq.message}</p>
                      </div>
                    )}

                    {/* Notas internas */}
                    <div>
                      <p className="text-gray-400 text-xs font-medium mb-1">Notas internas:</p>
                      <textarea
                        defaultValue={inq.admin_notes}
                        onBlur={(e) => handleNoteSave(inq.id, e.target.value)}
                        placeholder="Escribí notas internas..."
                        rows={2}
                        className="input-field text-sm resize-none"
                      />
                    </div>

                    {/* Botones de status */}
                    <div className="flex gap-2 flex-wrap">
                      {['pending', 'contacted', 'closed'].map((s) => {
                        const info = STATUS_MAP[s];
                        return (
                          <button
                            key={s}
                            onClick={() => handleStatusChange(inq.id, s)}
                            disabled={inq.status === s}
                            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                              inq.status === s
                                ? `bg-${info.color}-500/30 text-${info.color}-300 cursor-default`
                                : 'bg-white/5 text-gray-400 hover:bg-white/10'
                            }`}
                          >
                            {info.label}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
