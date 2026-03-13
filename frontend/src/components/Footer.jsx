import { Plane } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-[#0a0a0c] border-t border-white/5 py-8 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Plane className="w-5 h-5 text-purple-400" />
            <span className="text-sm font-semibold text-white">Aerowise</span>
          </div>
          <p className="text-xs text-gray-500">
            © {new Date().getFullYear()} Aerowise — Empty Legs de Aviación Privada. Todos los derechos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
}
