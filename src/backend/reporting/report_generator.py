import datetime
import logging
from flask import Flask, request, jsonify
# Assuming MOD-PRODUCT-DATA-MANAGEMENT provides a way to access data
# Replace with actual import from the other module
from src.backend.product_data_management import get_sales_data

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def validate_date_range(date_range):
    """
    Validates the date range string.
    Expected format: "YYYY-MM-DD,YYYY-MM-DD"
    """
    try:
        start_date_str, end_date_str = date_range.split(',')
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        if start_date > end_date:
            return False, "Start date cannot be after end date."
        return True, None
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD,YYYY-MM-DD"


def generate_product_performance_report(start_date, end_date):
    """
    Generates a product performance report based on the given date range.
    """
    try:
        # Fetch sales data from the product data management module
        sales_data = get_sales_data(start_date, end_date)

        # Process the sales data to generate the report
        report_data = []
        product_sales = {}
        for sale in sales_data:
            product_id = sale['product_id']
            quantity = sale['quantity']
            if product_id in product_sales:
                product_sales[product_id] += quantity
            else:
                product_sales[product_id] = quantity

        for product_id, total_sales in product_sales.items():
            report_data.append({
                'product_id': product_id,
                'total_sales': total_sales
            })

        return report_data

    except Exception as e:
        logging.error(f"Error generating report: {e}")
        # Implement notification to operations team here (e.g., via email or Slack)
        return None



@app.route('/reports/product-performance', methods=['GET'])
def product_performance_report():
    """
    API endpoint for generating product performance reports.
    """
    date_range = request.args.get('date_range')

    if not date_range:
        return jsonify({'error': 'Date range is required'}), 400

    is_valid, error_message = validate_date_range(date_range)
    if not is_valid:
        return jsonify({'error': error_message}), 400

    try:
        start_date_str, end_date_str = date_range.split(',')
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

        report_data = generate_product_performance_report(start_date, end_date)

        if report_data is None:
            return jsonify({'error': 'Report generation failed'}), 500

        return jsonify({'report_data': report_data}), 200

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)