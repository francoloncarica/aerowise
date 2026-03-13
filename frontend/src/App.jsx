import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import PanelLayout from './layouts/PanelLayout';
import PanelLogin from './components/PanelLogin';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './pages/LandingPage';
import PanelDashboard from './pages/PanelDashboard';
import PanelInquiries from './pages/PanelInquiries';
import PanelEmptyLegs from './pages/PanelEmptyLegs';
import PanelSources from './pages/PanelSources';

function RequireAuth({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <PanelLogin />;
  }

  return children;
}

function AppRoutes() {
  return (
    <Routes>
      {/* Landing pública */}
      <Route
        path="/"
        element={
          <>
            <Navbar />
            <LandingPage />
            <Footer />
          </>
        }
      />

      {/* Panel del dueño */}
      <Route
        path="/panel"
        element={
          <RequireAuth>
            <PanelLayout />
          </RequireAuth>
        }
      >
        <Route index element={<PanelDashboard />} />
        <Route path="inquiries" element={<PanelInquiries />} />
        <Route path="empty-legs" element={<PanelEmptyLegs />} />
        <Route path="sources" element={<PanelSources />} />
      </Route>

      {/* Redirect */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}
