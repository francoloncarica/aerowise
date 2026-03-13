import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  MessageSquare,
  Plane,
  Radio,
  ExternalLink,
  LogOut,
} from 'lucide-react';

const navItems = [
  { to: '/panel', icon: LayoutDashboard, label: 'Dashboard', end: true },
  { to: '/panel/inquiries', icon: MessageSquare, label: 'Consultas' },
  { to: '/panel/empty-legs', icon: Plane, label: 'Empty Legs' },
  { to: '/panel/sources', icon: Radio, label: 'Fuentes' },
];

export default function PanelLayout() {
  const { logout, token } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const { panelLogout } = await import('../api');
      await panelLogout(token);
    } catch {
      // Ignorar error
    }
    logout();
    navigate('/panel');
  };

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="w-[60px] lg:w-[220px] bg-[#111114] border-r border-white/5 flex flex-col fixed h-full z-40">
        {/* Logo */}
        <div className="p-3 lg:p-4 border-b border-white/5">
          <div className="flex items-center gap-2">
            <Plane className="w-6 h-6 text-purple-400 flex-shrink-0" />
            <span className="hidden lg:block text-lg font-bold text-white">
              Aerowise
              <span className="ml-2 text-[10px] bg-purple-600/30 text-purple-300 px-1.5 py-0.5 rounded-full font-normal">
                Panel
              </span>
            </span>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 py-4 space-y-1">
          {navItems.map(({ to, icon: Icon, label, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `flex items-center gap-3 mx-2 px-3 py-2.5 rounded-xl text-sm transition-colors ${
                  isActive
                    ? 'bg-purple-600/20 text-purple-400'
                    : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
                }`
              }
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              <span className="hidden lg:block">{label}</span>
            </NavLink>
          ))}
        </nav>

        {/* Footer */}
        <div className="p-3 lg:p-4 border-t border-white/5 space-y-2">
          <a
            href="/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-xs text-gray-500 hover:text-gray-300 transition-colors"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            <span className="hidden lg:block">Ver landing</span>
          </a>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 text-xs text-gray-500 hover:text-red-400 transition-colors w-full"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span className="hidden lg:block">Cerrar sesión</span>
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 ml-[60px] lg:ml-[220px] p-6 lg:p-8">
        <Outlet />
      </main>
    </div>
  );
}
