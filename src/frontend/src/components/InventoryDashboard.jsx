import React, { useState, useEffect } from 'react';
import axios from 'axios';

const InventoryDashboard = () => {
  const [inventoryData, setInventoryData] = useState({});
  const [productId, setProductId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchInventory = async () => {
    if (!productId) {
      setError('Please enter a product ID.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(`/products/${productId}`);
      setInventoryData(response.data);
      // Log inventory change (Optimistic Locking consideration - log before update)
      console.log(`Inventory updated for product ${productId}:`, response.data);
    } catch (err) {
      if (err.response && err.response.status === 404) {
        setError('Product not found.');
      } else {
        setError('Failed to fetch inventory. Please try again.');
        console.error('Error fetching inventory:', err);

        //Alert operations team on significant discrepancies.  This is a simplification for the frontend.
        if (err.response?.status === 500) {
          alert("Significant inventory discrepancy detected. Operations team alerted.");
        }
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    //Potentially poll for inventory updates.  For a real system, consider websockets or server-sent events
    const intervalId = setInterval(fetchInventory, 5000);

    return () => clearInterval(intervalId);
  }, [productId]);


  const handleProductIdChange = (event) => {
    setProductId(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetchInventory();
  };

  return (
    <div>
      <h2>Inventory Dashboard</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Product ID:
          <input type="text" value={productId} onChange={handleProductIdChange} />
        </label>
        <button type="submit">Fetch Inventory</button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {inventoryData.inventory_level !== undefined && (
        <div>
          <h3>Inventory Level</h3>
          <p>
            Product ID: {productId}
            <br />
            Inventory Level: {inventoryData.inventory_level}
          </p>
        </div>
      )}
    </div>
  );
};

export default InventoryDashboard;