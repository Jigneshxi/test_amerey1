import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SupplierList = () => {
  const [suppliers, setSuppliers] = useState([]);
  const [newSupplierName, setNewSupplierName] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchSuppliers = async () => {
      try {
        const response = await axios.get('/suppliers');
        setSuppliers(response.data);
      } catch (err) {
        console.error("Error fetching suppliers:", err);
        setError("Failed to fetch suppliers.");
      }
    };

    fetchSuppliers();
  }, []);

  const handleCreateSupplier = async () => {
    // Input validation to prevent injection attacks
    if (!newSupplierName || typeof newSupplierName !== 'string' || newSupplierName.length > 255) {
      setError("Invalid supplier name.  Name must be a string and less than 256 characters.");
      return;
    }

    try {
      const response = await axios.post('/suppliers', { name: newSupplierName });
      setSuppliers([...suppliers, response.data]);
      setNewSupplierName('');
      setError('');
    } catch (err) {
      console.error("Error creating supplier:", err);
      setError("Failed to create supplier.");
    }
  };

  const handleDeleteSupplier = async (id) => {
    try {
      //In a real application, you'd send a DELETE request to the backend.
      //For this example, we'll just filter the suppliers array.
      setSuppliers(suppliers.filter((supplier) => supplier.id !== id));
    } catch (err) {
      console.error("Error deleting supplier:", err);
      setError("Failed to delete supplier.");
    }
  };

  return (
    <div>
      <h2>Supplier List</h2>
      {error && <div className="error">{error}</div>}
      <ul>
        {suppliers.map((supplier) => (
          <li key={supplier.id}>
            {supplier.name}
            <button onClick={() => handleDeleteSupplier(supplier.id)}>Delete</button>
          </li>
        ))}
      </ul>
      <div>
        <input
          type="text"
          value={newSupplierName}
          onChange={(e) => setNewSupplierName(e.target.value)}
          placeholder="Enter supplier name"
        />
        <button onClick={handleCreateSupplier}>Create Supplier</button>
      </div>
    </div>
  );
};

export default SupplierList;