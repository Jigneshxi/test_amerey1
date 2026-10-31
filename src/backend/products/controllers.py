from flask import Flask, request, jsonify
import uuid
from src.backend.products.models import Product, ProductData
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/products', methods=['GET'])
def get_products():
    """
    Retrieves a list of all products.
    """
    try:
        products = Product.query.all()
        product_list = []
        for product in products:
            product_list.append({
                "id": str(product.id),
                "name": product.name
            })
        return jsonify(product_list), 200
    except Exception as e:
        logging.error(f"Error retrieving products: {e}")
        return jsonify({"error": "Failed to retrieve products"}), 500

@app.route('/products', methods=['POST'])
def create_product():
    """
    Creates a new product.
    """
    try:
        data = request.get_json()
        
        # Input validation to prevent injection attacks
        if not isinstance(data, dict) or 'name' not in data:
            logging.warning("Invalid request body. Missing 'name' field.")
            return jsonify({"error": "Invalid request body. 'name' is required."}), 400

        name = data['name']

        if not isinstance(name, str) or not name.strip():
            logging.warning("Invalid product name.")
            return jsonify({"error": "Invalid product name. Name must be a non-empty string."}), 400

        # Create a new product
        product_id = str(uuid.uuid4())
        new_product = Product(id=product_id, name=name)
        
        # Create corresponding product data entry
        product_data = ProductData(product_id=product_id, name=name)
        
        #Persist
        new_product.save()
        product_data.save()

        return jsonify({
            "id": product_id,
            "name": name
        }), 201
    except Exception as e:
        logging.error(f"Error creating product: {e}")
        return jsonify({"error": f"Failed to create product: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)