import { Plane } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0d0d0f]/80 backdrop-blur-xl border-b border-white/5">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center h-16">
          <a href="/" className="flex items-center gap-2.5">
            <Plane className="w-7 h-7 text-purple-400" />
            <span className="text-xl font-bold text-white tracking-tight">
              Aerowise
            </span>
          </a>
        </div>
      </div>
    </nav>
  );
}
