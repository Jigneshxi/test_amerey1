import React, { useState, useEffect } from 'react';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [newProductName, setNewProductName] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await fetch('/products');
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Failed to fetch products:', error);
      setError('Failed to fetch products. Please try again later.');
    }
  };

  const handleCreateProduct = async () => {
    // Input validation to prevent injection attacks
    if (!newProductName || typeof newProductName !== 'string' || newProductName.length > 255) {
      setError('Invalid product name. Name must be a string and less than 256 characters.');
      return;
    }

    try {
      const response = await fetch('/products', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: newProductName }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setProducts([...products, data]);
      setNewProductName('');
      setError(''); // Clear any previous errors
    } catch (error) {
      console.error('Failed to create product:', error);
      setError('Failed to create product. Please try again later.');
    }
  };

  const handleDeleteProduct = async (productId) => {
    try {
      // Implement delete functionality here (requires API endpoint)
      // For now, just remove from the local state
      setProducts(products.filter((product) => product.id !== productId));
    } catch (error) {
      console.error('Failed to delete product:', error);
      setError('Failed to delete product. Please try again later.');
    }
  };


  return (
    <div>
      <h1>Product List</h1>
      {error && <div className="error">{error}</div>}

      <input
        type="text"
        value={newProductName}
        onChange={(e) => setNewProductName(e.target.value)}
        placeholder="Enter product name"
      />
      <button onClick={handleCreateProduct}>Create Product</button>

      <ul>
        {products.map((product) => (
          <li key={product.id}>
            {product.name}
            <button onClick={() => handleDeleteProduct(product.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProductList;