import React, { useState } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { MessageSquare, Map, Menu, X, Radio } from 'lucide-react';
import ConsultaPage from './pages/ConsultaPage.jsx';
import MapaPage from './pages/MapaPage.jsx';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  const isLinkActive = (path) => {
    return location.pathname === path || (path === '/' && location.pathname === '/index.html');
  };

  return (
    <div className="app-container">
      <header className="mobile-header">
        <div className="sidebar-logo">
          <Radio size={24} color="#06b6d4" />
          <span>AppBit Painel</span>
        </div>
        <button className="menu-toggle" onClick={toggleSidebar} aria-label="Toggle menu">
          {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </header>

      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <Radio size={28} color="#06b6d4" />
            <span>AppBit Painel</span>
          </div>
        </div>

        <nav style={{ flex: 1 }}>
          <ul className="sidebar-menu">
            <li className={`sidebar-item ${isLinkActive('/') ? 'active' : ''}`} onClick={closeSidebar}>
              <Link to="/">
                <MessageSquare size={20} />
                <span>Consulta Inteligente</span>
              </Link>
            </li>
            <li className={`sidebar-item ${isLinkActive('/mapa') ? 'active' : ''}`} onClick={closeSidebar}>
              <Link to="/mapa">
                <Map size={20} />
                <span>Mapa Interativo</span>
              </Link>
            </li>
          </ul>
        </nav>

        <div className="sidebar-footer">
          <p>© 2026 AppBit Angola</p>
          <p style={{ fontSize: '0.65rem', marginTop: '4px' }}>v0.1.0 (CDRView TechRef)</p>
        </div>
      </aside>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<ConsultaPage />} />
          <Route path="/mapa" element={<MapaPage />} />
          <Route path="*" element={<ConsultaPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
