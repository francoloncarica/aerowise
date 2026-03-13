import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { fetchSources, triggerScrape } from '../api';
import {
  Globe, Mail, MessageCircle, Edit3, Loader2,
  CheckCircle, XCircle, ExternalLink, RefreshCw,
} from 'lucide-react';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';

const TYPE_ICONS = {
  web_scraping: Globe,
  email: Mail,
  whatsapp: MessageCircle,
  manual: Edit3,
};

const TYPE_LABELS = {
  web_scraping: 'Web Scraping',
  email: 'Email',
  whatsapp: 'WhatsApp',
  manual: 'Manual',
};

export default function PanelSources() {
  const { token } = useAuth();
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [scraping, setScraping] = useState({});

  const load = async () => {
    setLoading(true);
    try {
      const res = await fetchSources(token);
      setSources(res.data.results || res.data);
    } catch {
      setSources([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [token]);

  const handleScrape = async (id) => {
    setScraping((prev) => ({ ...prev, [id]: true }));
    try {
      await triggerScrape(id, token);
      await load();
    } catch {
      // Ignorar
    } finally {
      setScraping((prev) => ({ ...prev, [id]: false }));
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-white">Fuentes</h1>
        <span className="text-gray-500 text-sm">{sources.length} fuentes configuradas</span>
      </div>

      {sources.length === 0 ? (
        <div className="text-center py-20">
          <Globe className="w-12 h-12 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-500">No hay fuentes configuradas.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {sources.map((source) => {
            const Icon = TYPE_ICONS[source.source_type] || Globe;
            const isScraping = scraping[source.id];

            return (
              <div key={source.id} className="glass-card p-5 group">
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg ${
                      source.is_active
                        ? 'bg-purple-500/20 text-purple-400'
                        : 'bg-white/5 text-gray-600'
                    }`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-white font-semibold text-sm leading-tight">
                        {source.name || source.operator_name || `Fuente #${source.id}`}
                      </h3>
                      <span className="text-[10px] text-gray-500 uppercase tracking-wider">
                        {TYPE_LABELS[source.source_type] || source.source_type}
                      </span>
                    </div>
                  </div>
                  <span className={`text-[10px] px-2 py-0.5 rounded-full ${
                    source.is_active
                      ? 'bg-green-500/20 text-green-400'
                      : 'bg-red-500/20 text-red-400'
                  }`}>
                    {source.is_active ? 'Activa' : 'Inactiva'}
                  </span>
                </div>

                {/* URL */}
                {source.url && (
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-purple-400 transition-colors mb-3 truncate"
                  >
                    <ExternalLink className="w-3 h-3 flex-shrink-0" />
                    <span className="truncate">{source.url}</span>
                  </a>
                )}

                {/* Stats */}
                <div className="space-y-2 mb-4 text-xs">
                  {source.operator_name && (
                    <div className="flex justify-between text-gray-500">
                      <span>Operador</span>
                      <span className="text-gray-300">{source.operator_name}</span>
                    </div>
                  )}
                  <div className="flex justify-between text-gray-500">
                    <span>Último scraping</span>
                    <span className="text-gray-300">
                      {source.last_scraped_at
                        ? format(parseISO(source.last_scraped_at), "d MMM, HH:mm", { locale: es })
                        : 'Nunca'}
                    </span>
                  </div>
                  {source.legs_found != null && (
                    <div className="flex justify-between text-gray-500">
                      <span>Legs encontrados</span>
                      <span className="text-gray-300">{source.legs_found}</span>
                    </div>
                  )}
                  <div className="flex justify-between text-gray-500">
                    <span>Errores consecutivos</span>
                    <span className={source.consecutive_errors > 0 ? 'text-red-400' : 'text-gray-300'}>
                      {source.consecutive_errors || 0}
                    </span>
                  </div>
                </div>

                {/* Status Badges */}
                <div className="flex items-center gap-2 mb-4">
                  {source.last_success_at && (
                    <div className="flex items-center gap-1 text-[10px] text-green-400">
                      <CheckCircle className="w-3 h-3" />
                      <span>Éxito previo</span>
                    </div>
                  )}
                  {source.consecutive_errors > 0 && (
                    <div className="flex items-center gap-1 text-[10px] text-red-400">
                      <XCircle className="w-3 h-3" />
                      <span>{source.consecutive_errors} errores</span>
                    </div>
                  )}
                </div>

                {/* Scrape Button */}
                {source.source_type === 'web_scraping' && source.is_active && (
                  <button
                    onClick={() => handleScrape(source.id)}
                    disabled={isScraping}
                    className="btn-secondary w-full text-sm flex items-center justify-center gap-2 disabled:opacity-50"
                  >
                    {isScraping ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Scrapeando...
                      </>
                    ) : (
                      <>
                        <RefreshCw className="w-4 h-4" />
                        Scrape ahora
                      </>
                    )}
                  </button>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
