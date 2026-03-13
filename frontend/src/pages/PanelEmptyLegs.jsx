import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { fetchEmptyLegs, toggleEmptyLeg } from '../api';
import {
  ShieldCheck, ShieldOff, Eye, EyeOff, ArrowRight,
  ChevronLeft, ChevronRight, Plane,
} from 'lucide-react';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';

export default function PanelEmptyLegs() {
  const { token } = useAuth();
  const [legs, setLegs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [filters, setFilters] = useState({
    status: '',
    verified: '',
    published: '',
  });

  const load = async () => {
    setLoading(true);
    try {
      const params = { page };
      if (filters.status) params.status = filters.status;
      if (filters.verified) params.verified = filters.verified;
      if (filters.published) params.published = filters.published;

      const res = await fetchEmptyLegs(params, token);
      setLegs(res.data.results || res.data);
      setTotal(res.data.count || (res.data.results || res.data).length);
    } catch {
      setLegs([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [page, filters, token]);

  const handleToggle = async (id, field) => {
    try {
      const res = await toggleEmptyLeg(id, field, token);
      setLegs((prev) =>
        prev.map((leg) => (leg.id === id ? res.data : leg))
      );
    } catch {
      // Ignorar
    }
  };

  const pageSize = 50;
  const totalPages = Math.ceil(total / pageSize);

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-6">Empty Legs</h1>

      {/* Filtros */}
      <div className="flex gap-3 mb-6 flex-wrap">
        <select
          className="input-field w-auto text-sm"
          value={filters.status}
          onChange={(e) => { setFilters({ ...filters, status: e.target.value }); setPage(1); }}
        >
          <option value="">Todos los estados</option>
          <option value="available">Disponible</option>
          <option value="booked">Reservado</option>
          <option value="expired">Expirado</option>
          <option value="cancelled">Cancelado</option>
        </select>
        <select
          className="input-field w-auto text-sm"
          value={filters.verified}
          onChange={(e) => { setFilters({ ...filters, verified: e.target.value }); setPage(1); }}
        >
          <option value="">Verificación</option>
          <option value="true">Verificado</option>
          <option value="false">No verificado</option>
        </select>
        <select
          className="input-field w-auto text-sm"
          value={filters.published}
          onChange={(e) => { setFilters({ ...filters, published: e.target.value }); setPage(1); }}
        >
          <option value="">Publicación</option>
          <option value="true">Publicado</option>
          <option value="false">No publicado</option>
        </select>
      </div>

      {loading ? (
        <div className="flex justify-center py-20">
          <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : legs.length === 0 ? (
        <div className="text-center py-20">
          <Plane className="w-12 h-12 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-500">No hay empty legs con estos filtros.</p>
        </div>
      ) : (
        <>
          {/* Tabla */}
          <div className="glass-card overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/5">
                    <th className="text-left text-gray-500 font-medium px-4 py-3 text-xs">Ruta</th>
                    <th className="text-left text-gray-500 font-medium px-4 py-3 text-xs">Fecha</th>
                    <th className="text-left text-gray-500 font-medium px-4 py-3 text-xs">Aeronave</th>
                    <th className="text-right text-gray-500 font-medium px-4 py-3 text-xs">Precio USD</th>
                    <th className="text-right text-gray-500 font-medium px-4 py-3 text-xs">Desc.</th>
                    <th className="text-left text-gray-500 font-medium px-4 py-3 text-xs">Operador</th>
                    <th className="text-center text-gray-500 font-medium px-4 py-3 text-xs">Estado</th>
                    <th className="text-center text-gray-500 font-medium px-4 py-3 text-xs">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {legs.map((leg) => (
                    <tr key={leg.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-1.5">
                          <span className="text-gray-200 whitespace-nowrap">{leg.origin_display || leg.origin_raw}</span>
                          <ArrowRight className="w-3 h-3 text-purple-400" />
                          <span className="text-gray-200 whitespace-nowrap">{leg.destination_display || leg.destination_raw}</span>
                        </div>
                      </td>
                      <td className="px-4 py-3 text-gray-400 whitespace-nowrap">
                        {format(parseISO(leg.departure_date), "d MMM ''yy", { locale: es })}
                      </td>
                      <td className="px-4 py-3 text-gray-400">
                        {leg.aircraft_display || leg.aircraft_raw || '—'}
                      </td>
                      <td className="px-4 py-3 text-right">
                        {leg.price_usd ? (
                          <span className="text-purple-400 font-medium">
                            ${Number(leg.price_usd).toLocaleString()}
                          </span>
                        ) : (
                          <span className="text-gray-600">—</span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-right">
                        {leg.discount_percent ? (
                          <span className="text-green-400">{leg.discount_percent}%</span>
                        ) : (
                          <span className="text-gray-600">—</span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-gray-400 text-xs">
                        {leg.operator_display || leg.operator || '—'}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span
                          className={`text-[10px] px-2 py-0.5 rounded-full ${
                            leg.status === 'available'
                              ? 'bg-green-500/20 text-green-400'
                              : leg.status === 'booked'
                              ? 'bg-yellow-500/20 text-yellow-400'
                              : 'bg-red-500/20 text-red-400'
                          }`}
                        >
                          {leg.status}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center justify-center gap-1">
                          <button
                            onClick={() => handleToggle(leg.id, 'verified')}
                            title={leg.verified ? 'Quitar verificación' : 'Verificar'}
                            className={`p-1.5 rounded-lg transition-colors ${
                              leg.verified
                                ? 'bg-blue-500/20 text-blue-400 hover:bg-blue-500/30'
                                : 'bg-white/5 text-gray-500 hover:bg-white/10'
                            }`}
                          >
                            {leg.verified ? (
                              <ShieldCheck className="w-4 h-4" />
                            ) : (
                              <ShieldOff className="w-4 h-4" />
                            )}
                          </button>
                          <button
                            onClick={() => handleToggle(leg.id, 'published')}
                            title={leg.published ? 'Despublicar' : 'Publicar'}
                            className={`p-1.5 rounded-lg transition-colors ${
                              leg.published
                                ? 'bg-purple-500/20 text-purple-400 hover:bg-purple-500/30'
                                : 'bg-white/5 text-gray-500 hover:bg-white/10'
                            }`}
                          >
                            {leg.published ? (
                              <Eye className="w-4 h-4" />
                            ) : (
                              <EyeOff className="w-4 h-4" />
                            )}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Paginación */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between mt-4">
              <p className="text-gray-500 text-xs">{total} resultados</p>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setPage(Math.max(1, page - 1))}
                  disabled={page === 1}
                  className="btn-secondary p-2 disabled:opacity-30"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <span className="text-gray-400 text-sm">
                  {page} / {totalPages}
                </span>
                <button
                  onClick={() => setPage(Math.min(totalPages, page + 1))}
                  disabled={page === totalPages}
                  className="btn-secondary p-2 disabled:opacity-30"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
