import functools
import logging
from flask import request, jsonify
from src.backend.api.api_keys import verify_api_key, revoke_api_key  # Assuming MOD-001 is implemented as api_keys.py
from flask_limiter import Limiter
from flask_limiter.decorators import limit

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize rate limiter
limiter = Limiter(app=None, key_func=lambda: request.remote_addr, default_limits=["30/minute"])  # Replace None with your Flask app instance

def token_required(f):
    """
    Decorator to protect API endpoints with API key authentication.
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            logging.warning("No API key provided.")
            return jsonify({'message': 'API key missing'}), 401

        try:
            user_id = verify_api_key(api_key)
            if user_id is None:
                logging.warning(f"Invalid API key: {api_key}")
                return jsonify({'message': 'Invalid API key'}), 401
            
            request.user_id = user_id  # Attach user_id to the request context for authorization
        except Exception as e:
            logging.error(f"Error verifying API key: {e}")
            return jsonify({'message': 'Internal server error'}), 500

        return f(*args, **kwargs)
    return wrapper

def permission_required(permission):
    """
    Decorator to check if the user has the required permission.  This is a placeholder.  
    A real implementation would likely check user roles or permissions associated with the API key.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            user_id = request.user_id  # Assuming user_id is set by token_required
            # Placeholder permission check:
            if user_id != "admin":  # Example: Only admin can access this endpoint
                logging.warning(f"User {user_id} does not have permission to access this resource.")
                return jsonify({'message': 'Forbidden'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator


def handle_api_key_compromise(api_key):
    """
    Handles API key compromise by revoking the key.
    """
    try:
        revoke_api_key(api_key)
        logging.warning(f"API key compromised and revoked: {api_key}")
    except Exception as e:
        logging.error(f"Error revoking API key: {e}")

def log_request(req, res):
    """Logs request and response details."""
    logging.info(f"Request: {req.method} {req.url} - Headers: {req.headers} - Body: {req.get_data(as_text=True)}")
    logging.info(f"Response: {res.status} - Body: {res.get_data(as_text=True)}")


# Example usage:
# @token_required
# @permission_required("read:data")
# def my_api_endpoint():
#     # ... your API logic ...

# Add the logging middleware to the Flask app
# from flask import Flask
# app = Flask(__name__)
# app.after_request(log_request)
# limiter.init_app(app) # Initialize the limiter with your Flask app