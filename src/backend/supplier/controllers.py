from flask import Flask, request, jsonify
import uuid
import logging

app = Flask(__name__)

# In-memory data store (replace with a database in a production environment)
suppliers = {}

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/suppliers', methods=['GET'])
def get_suppliers():
    """
    Retrieves a list of all suppliers.
    """
    supplier_list = []
    for supplier_id, supplier_data in suppliers.items():
        supplier_list.append({
            'id': supplier_id,
            'name': supplier_data['name']
        })
    return jsonify(supplier_list), 200

@app.route('/suppliers', methods=['POST'])
def create_supplier():
    """
    Creates a new supplier.
    """
    try:
        data = request.get_json()
        
        # Input validation to prevent injection attacks
        if not isinstance(data, dict) or 'name' not in data:
            return jsonify({'error': 'Invalid request body.  "name" is required.'}), 400
        
        name = data['name']
        if not isinstance(name, str) or not name.strip():
            return jsonify({'error': 'Supplier name must be a non-empty string.'}), 400

        supplier_id = str(uuid.uuid4())
        suppliers[supplier_id] = {'name': name}
        logging.info(f"Created supplier with ID: {supplier_id} and name: {name}")
        return jsonify({'id': supplier_id, 'name': name}), 201
    except Exception as e:
        logging.error(f"Error creating supplier: {e}")
        return jsonify({'error': 'Failed to create supplier.'}), 500

if __name__ == '__main__':
    app.run(debug=True)