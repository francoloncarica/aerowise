import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { fetchDashboardStats } from '../api';
import {
  Plane, MessageSquare, Radio, TrendingDown,
  ArrowRight, DollarSign,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function PanelDashboard() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardStats(token)
      .then((res) => setStats(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [token]);

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!stats) {
    return <p className="text-gray-500">Error cargando estadísticas.</p>;
  }

  const statCards = [
    { label: 'Legs disponibles', value: stats.total_legs, icon: Plane, color: 'purple' },
    { label: 'Consultas pendientes', value: stats.pending_inquiries, icon: MessageSquare, color: 'yellow' },
    { label: 'Fuentes activas', value: stats.active_sources, icon: Radio, color: 'green' },
    { label: 'Descuento promedio', value: `${stats.avg_discount}%`, icon: TrendingDown, color: 'blue' },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-6">Dashboard</h1>

      {/* Stat cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {statCards.map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="glass-card p-5">
            <div className="flex items-center justify-between mb-3">
              <span className="text-gray-400 text-xs">{label}</span>
              <Icon className={`w-5 h-5 text-${color}-400`} />
            </div>
            <p className="text-2xl font-bold text-white">{value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Leg más barato */}
        {stats.cheapest && (
          <div className="glass-card p-6">
            <h3 className="text-sm font-semibold text-gray-400 mb-4 flex items-center gap-2">
              <DollarSign className="w-4 h-4" />
              Empty Leg más barato
            </h3>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-white font-semibold">
                {stats.cheapest.origin_display}
              </span>
              <ArrowRight className="w-4 h-4 text-purple-400" />
              <span className="text-white font-semibold">
                {stats.cheapest.destination_display}
              </span>
            </div>
            <p className="text-purple-400 text-2xl font-bold mb-1">
              US$ {Number(stats.cheapest.price_usd).toLocaleString()}
            </p>
            <p className="text-gray-500 text-xs">
              {stats.cheapest.departure_date} — {stats.cheapest.aircraft_display || 'Aeronave por confirmar'}
            </p>
          </div>
        )}

        {/* Top rutas */}
        <div className="glass-card p-6">
          <h3 className="text-sm font-semibold text-gray-400 mb-4">Rutas más frecuentes</h3>
          <div className="space-y-3">
            {stats.top_routes.map((route, i) => (
              <div key={i} className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-gray-500 w-5">{i + 1}.</span>
                  <span className="text-gray-300">{route.origin_raw}</span>
                  <ArrowRight className="w-3 h-3 text-purple-400" />
                  <span className="text-gray-300">{route.destination_raw}</span>
                </div>
                <span className="text-purple-400 text-sm font-medium">{route.count}</span>
              </div>
            ))}
            {stats.top_routes.length === 0 && (
              <p className="text-gray-600 text-sm">Sin datos</p>
            )}
          </div>
        </div>
      </div>

      {/* Últimas consultas pendientes */}
      <div className="glass-card p-6 mt-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-gray-400">Últimas consultas pendientes</h3>
          <button
            onClick={() => navigate('/panel/inquiries')}
            className="text-xs text-purple-400 hover:text-purple-300"
          >
            Ver todas →
          </button>
        </div>
        <div className="space-y-3">
          {stats.recent_inquiries.map((inq) => (
            <div key={inq.id} className="flex items-center justify-between py-2 border-b border-white/5 last:border-0">
              <div>
                <p className="text-sm text-white">{inq.name}</p>
                <p className="text-xs text-gray-500">{inq.email} — {inq.empty_leg_display}</p>
              </div>
              <span className="text-[10px] bg-yellow-500/20 text-yellow-400 px-2 py-0.5 rounded-full">
                Pendiente
              </span>
            </div>
          ))}
          {stats.recent_inquiries.length === 0 && (
            <p className="text-gray-600 text-sm">Sin consultas pendientes</p>
          )}
        </div>
      </div>
    </div>
  );
}
