from flask import Flask, request, jsonify
import logging
from src.backend.product_data.enrichment.services import enrich_product_data
from src.backend.product_data.enrichment.models import ProductAttributes

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/enrich', methods=['POST'])
def enrich_endpoint():
    """
    Enriches product data from a request and stores it in the ProductAttributes table.
    """
    try:
        product_data = request.get_json()
        if not product_data or 'product_id' not in product_data:
            return jsonify({'error': 'Invalid product data. product_id is required.'}), 400

        product_id = product_data['product_id']

        try:
            enriched_data = enrich_product_data(product_id)
            if enriched_data:
                # Assuming ProductAttributes model has a method to save the data
                ProductAttributes.save_attributes(product_id, enriched_data)
                return jsonify({'message': 'Product data enriched and saved successfully'}), 200
            else:
                return jsonify({'message': 'Product data enrichment returned no results.'}), 200

        except Exception as e:
            logging.error(f"Error during enrichment for product_id {product_id}: {e}")
            return jsonify({'error': f'Error enriching product data: {e}'}), 500

    except Exception as e:
        logging.exception("Unexpected error in enrich_endpoint")
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)