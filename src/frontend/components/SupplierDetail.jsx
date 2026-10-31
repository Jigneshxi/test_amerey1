import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SupplierDetail = ({ supplierId }) => {
  const [supplier, setSupplier] = useState(null);
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSupplier = async () => {
      try {
        const response = await axios.get(`/suppliers/${supplierId}`);
        setSupplier(response.data);
        setName(response.data.name);
      } catch (err) {
        setError(err.message);
        setSupplier(null);
      } finally {
        setLoading(false);
      }
    };

    fetchSupplier();
  }, [supplierId]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Input validation to prevent injection attacks
    if (!name || typeof name !== 'string' || name.length > 255) {
      setError("Invalid supplier name. Name must be a string and less than 256 characters.");
      return;
    }
    
    try {
      const response = await axios.put(`/suppliers/${supplierId}`, { name });
      setSupplier(response.data);
      // Optionally, show a success message
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  if (!supplier) {
    return <p>Supplier not found.</p>;
  }

  return (
    <div>
      <h2>Supplier Details</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <button type="submit">Update Supplier</button>
      </form>
    </div>
  );
};

export default SupplierDetail;