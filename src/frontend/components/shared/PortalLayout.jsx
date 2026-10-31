import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import SupplierPortal from '../../portals/supplier/index.jsx';
import RetailerPortal from '../../portals/retailer/index.jsx';
import './PortalLayout.css'; // Create this CSS file for styling

function PortalLayout() {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768); // Adjust breakpoint as needed
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Initial check on mount

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <Router>
      <div className="portal-layout">
        <header className="portal-header">
          <div className="logo">
            <Link to="/" className="logo-link">Portal</Link>
          </div>
          <nav className={isMobile ? 'portal-nav-mobile' : 'portal-nav'}>
            <ul>
              <li>
                <Link to="/supplier">Supplier Portal</Link>
              </li>
              <li>
                <Link to="/retailer">Retailer Portal</Link>
              </li>
            </ul>
          </nav>
        </header>

        <main className="portal-main">
          <Routes>
            <Route path="/supplier" element={<SupplierPortal />} />
            <Route path="/retailer" element={<RetailerPortal />} />
            <Route path="/" element={<div>Welcome! Select a portal above.</div>} />
            <Route path="*" element={<div>Error 404: Page not found.</div>} />
          </Routes>
        </main>

        <footer className="portal-footer">
          <p>&copy; {new Date().getFullYear()} Your Company. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default PortalLayout;