import { useState, useEffect } from 'react';
import { Search, Plane, Shield, Bell, ArrowRight, HelpCircle } from 'lucide-react';
import EmptyLegCard from '../components/EmptyLegCard';
import InquiryModal from '../components/InquiryModal';
import SubscribeForm from '../components/SubscribeForm';
import { fetchPublicEmptyLegs } from '../api';

export default function LandingPage() {
  const [legs, setLegs] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [selectedLeg, setSelectedLeg] = useState(null);

  const loadLegs = async (query = '') => {
    setLoading(true);
    try {
      const res = await fetchPublicEmptyLegs(query);
      setLegs(res.data);
    } catch {
      setLegs([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLegs();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    loadLegs(search);
  };

  return (
    <div className="pt-16">
      {/* Hero */}
      <section className="hero-gradient py-20 sm:py-28 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white mb-4 leading-tight">
            Empty Legs
          </h1>
          <p className="text-lg sm:text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Volá en jets privados con hasta un <span className="text-purple-400 font-semibold">90% de descuento</span>.
            Centralizamos los mejores empty legs de operadores verificados.
          </p>

          {/* Buscador */}
          <form onSubmit={handleSearch} className="max-w-xl mx-auto relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Buscá por ciudad o país..."
              className="w-full pl-12 pr-32 py-4 bg-white/10 border border-white/10 rounded-2xl text-white placeholder-gray-400 focus:outline-none focus:border-purple-500/50 text-sm"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <button
              type="submit"
              className="absolute right-2 top-1/2 -translate-y-1/2 px-5 py-2.5 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-xl transition-colors"
            >
              Buscar
            </button>
          </form>
        </div>
      </section>

      {/* Value props */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10 relative z-10">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            { icon: Plane, title: 'Hasta 90% OFF', desc: 'Descuentos reales en vuelos que de otra forma viajarían vacíos.' },
            { icon: Shield, title: 'Operadores verificados', desc: 'Trabajamos solo con compañías de aviación confiables.' },
            { icon: Bell, title: 'Alertas personalizadas', desc: 'Recibí notificaciones cuando haya vuelos a tu destino.' },
          ].map(({ icon: Icon, title, desc }) => (
            <div key={title} className="glass-card p-5 flex items-start gap-4">
              <div className="w-10 h-10 bg-purple-600/20 rounded-xl flex items-center justify-center flex-shrink-0">
                <Icon className="w-5 h-5 text-purple-400" />
              </div>
              <div>
                <h3 className="text-white font-semibold text-sm mb-1">{title}</h3>
                <p className="text-gray-400 text-xs">{desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Grid de empty legs */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-2xl font-bold text-white mb-8">Empty Legs disponibles</h2>

        {loading ? (
          <div className="flex justify-center py-20">
            <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : legs.length === 0 ? (
          <div className="text-center py-20">
            <Plane className="w-12 h-12 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-500">No hay empty legs disponibles en este momento.</p>
            {search && (
              <button
                onClick={() => { setSearch(''); loadLegs(); }}
                className="mt-4 text-purple-400 hover:text-purple-300 text-sm"
              >
                Ver todos los vuelos
              </button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {legs.map((leg) => (
              <EmptyLegCard
                key={leg.id}
                leg={leg}
                isPublic
                onInquiry={setSelectedLeg}
              />
            ))}
          </div>
        )}
      </section>

      {/* Suscripción */}
      <section className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <SubscribeForm />
      </section>

      {/* ¿Qué es un empty leg? */}
      <section className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <div className="glass-card p-6 sm:p-8">
          <div className="flex items-center gap-3 mb-4">
            <HelpCircle className="w-6 h-6 text-purple-400" />
            <h3 className="text-lg font-bold text-white">¿Qué es un empty leg?</h3>
          </div>
          <div className="space-y-3 text-gray-400 text-sm leading-relaxed">
            <p>
              Un <strong className="text-gray-200">empty leg</strong> (o "tramo vacío") es un vuelo de reposicionamiento
              de un jet privado que viaja sin pasajeros. Ocurre cuando un avión necesita trasladarse a otro aeropuerto
              para recoger pasajeros o volver a su base.
            </p>
            <p>
              En lugar de volar vacío, los operadores ofrecen estos tramos a <strong className="text-gray-200">precios
              significativamente reducidos</strong> — típicamente entre un 50% y un 90% menos que un vuelo chárter regular.
            </p>
            <p>
              Es una oportunidad única para volar en aviación privada a una fracción del costo. Las fechas y rutas son
              fijas, pero el ahorro es extraordinario.
            </p>
          </div>
        </div>
      </section>

      {/* Modal de consulta */}
      {selectedLeg && (
        <InquiryModal
          leg={selectedLeg}
          onClose={() => setSelectedLeg(null)}
        />
      )}
    </div>
  );
}
