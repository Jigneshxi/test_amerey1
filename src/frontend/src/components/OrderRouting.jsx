import React, { useState } from 'react';
import axios from 'axios';

const OrderRouting = () => {
  const [quantity, setQuantity] = useState(1);
  const [productId, setProductId] = useState('');
  const [customerLocation, setCustomerLocation] = useState('');
  const [orderId, setOrderId] = useState('');
  const [fulfillmentCenter, setFulfillmentCenter] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/orders', {
        quantity,
        product_id: productId,
        customer_location: customerLocation,
      });

      if (response.status === 202) {
        setOrderId(response.data.order_id);
        setFulfillmentCenter(response.data.fulfillment_center);
      } else {
        throw new Error(`Unexpected response status: ${response.status}`);
      }
    } catch (err) {
      if (err.response && err.response.status === 400) {
        setError('Invalid input. Please check your order details.');
      } else if (err.response && err.response.status === 500) {
        setError('Routing failure. Please try again later.');
        // Log the error and notify the operations team (replace with actual logging/notification)
        console.error('Order routing failed:', err);
        // Implement retry logic (example with exponential backoff)
        setTimeout(() => {
          console.log('Retrying order routing...');
          handleSubmit(e); // Retry the submission
        }, 2000); // Retry after 2 seconds
      }
      else {
        setError('An unexpected error occurred.');
        console.error('Order routing error:', err);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Order Routing</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="quantity">Quantity:</label>
          <input
            type="number"
            id="quantity"
            value={quantity}
            onChange={(e) => setQuantity(parseInt(e.target.value))}
            required
          />
        </div>
        <div>
          <label htmlFor="productId">Product ID:</label>
          <input
            type="text"
            id="productId"
            value={productId}
            onChange={(e) => setProductId(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="customerLocation">Customer Location:</label>
          <input
            type="text"
            id="customerLocation"
            value={customerLocation}
            onChange={(e) => setCustomerLocation(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Routing...' : 'Route Order'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {orderId && fulfillmentCenter && (
        <div>
          <h3>Order Confirmation</h3>
          <p>Order ID: {orderId}</p>
          <p>Fulfillment Center: {fulfillmentCenter}</p>
        </div>
      )}
    </div>
  );
};

export default OrderRouting;