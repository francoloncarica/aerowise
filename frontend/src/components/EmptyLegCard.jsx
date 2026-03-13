import { ArrowRight, Users, Calendar, Tag, Plane } from 'lucide-react';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';

export default function EmptyLegCard({ leg, isPublic = false, onInquiry }) {
  const formatDate = (dateStr) => {
    try {
      return format(parseISO(dateStr), "d 'de' MMM, yyyy", { locale: es });
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="leg-card p-5">
      {/* Ruta */}
      <div className="flex items-center gap-2 mb-3">
        <span className="text-white font-semibold text-sm truncate">
          {leg.origin_display || '—'}
        </span>
        <ArrowRight className="w-4 h-4 text-purple-400 flex-shrink-0" />
        <span className="text-white font-semibold text-sm truncate">
          {leg.destination_display || '—'}
        </span>
      </div>

      {/* Info */}
      <div className="space-y-2 mb-4">
        <div className="flex items-center gap-2 text-gray-400 text-xs">
          <Calendar className="w-3.5 h-3.5" />
          <span>{formatDate(leg.departure_date)}</span>
          {leg.departure_time && (
            <span className="text-gray-500">— {leg.departure_time.slice(0, 5)}</span>
          )}
        </div>

        {leg.aircraft_display && (
          <div className="flex items-center gap-2 text-gray-400 text-xs">
            <Plane className="w-3.5 h-3.5" />
            <span>{leg.aircraft_display}</span>
          </div>
        )}

        {leg.max_passengers && (
          <div className="flex items-center gap-2 text-gray-400 text-xs">
            <Users className="w-3.5 h-3.5" />
            <span>Hasta {leg.max_passengers} pasajeros</span>
          </div>
        )}
      </div>

      {isPublic ? (
        /* Vista pública: sin precio */
        <>
          <div className="flex items-center justify-between mb-4">
            <span className="text-purple-300 text-sm font-medium">Precio a consultar</span>
            {leg.has_discount && (
              <span className="text-[10px] bg-purple-600/20 text-purple-300 px-2 py-0.5 rounded-full">
                Con descuento
              </span>
            )}
          </div>
          <button
            onClick={() => onInquiry && onInquiry(leg)}
            className="w-full btn-primary text-sm py-2.5"
          >
            Me interesa
          </button>
        </>
      ) : (
        /* Vista admin: con precio */
        <>
          <div className="flex items-center justify-between mb-3">
            {leg.price_usd ? (
              <span className="text-purple-400 text-xl font-bold">
                US$ {Number(leg.price_usd).toLocaleString()}
              </span>
            ) : (
              <span className="text-gray-500 text-sm">Sin precio</span>
            )}
            {leg.discount_percent && (
              <span className="text-xs bg-green-500/20 text-green-400 px-2 py-0.5 rounded-full">
                -{leg.discount_percent}%
              </span>
            )}
          </div>

          {leg.operator_display && (
            <p className="text-gray-500 text-xs mb-2">
              <Tag className="w-3 h-3 inline mr-1" />
              {leg.operator_display}
            </p>
          )}

          <div className="flex gap-2 flex-wrap">
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
            {leg.verified && (
              <span className="text-[10px] bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded-full">
                Verificado
              </span>
            )}
            {leg.published && (
              <span className="text-[10px] bg-purple-500/20 text-purple-400 px-2 py-0.5 rounded-full">
                Publicado
              </span>
            )}
          </div>
        </>
      )}
    </div>
  );
}
