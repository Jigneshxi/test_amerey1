import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import PortalLayout from '../../components/shared/PortalLayout';
import SupplierDashboard from './SupplierDashboard';
import SupplierProducts from './SupplierProducts';
import SupplierOrders from './SupplierOrders';

function SupplierPortal() {
  return (
    <Router>
      <PortalLayout>
        <Routes>
          <Route path="/" element={<SupplierDashboard />} />
          <Route path="/products" element={<SupplierProducts />} />
          <Route path="/orders" element={<SupplierOrders />} />
        </Routes>
      </PortalLayout>
    </Router>
  );
}

export default SupplierPortal;