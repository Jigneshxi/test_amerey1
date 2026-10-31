import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import PortalLayout from '../../components/shared/PortalLayout';
import RetailerDashboard from './components/RetailerDashboard';
import RetailerOrders from './components/RetailerOrders';
import RetailerProducts from './components/RetailerProducts';

function RetailerPortal() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<PortalLayout />}>
          <Route index element={<RetailerDashboard />} />
          <Route path="orders" element={<RetailerOrders />} />
          <Route path="products" element={<RetailerProducts />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default RetailerPortal;