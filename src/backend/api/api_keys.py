import uuid
import hashlib
import datetime
from flask import Flask, request, jsonify
from functools import wraps

# Assuming MOD-001 is a database module (adapt as needed)
# from src.backend.database import db

app = Flask(__name__)

# In-memory storage for API keys (replace with database in production)
api_keys = {}


def generate_api_key():
    """Generates a unique API key."""
    api_key = str(uuid.uuid4())
    hashed_api_key = hashlib.sha256(api_key.encode()).hexdigest()
    return api_key, hashed_api_key


def create_api_key(user_id):
    """Creates a new API key for a user."""
    api_key, hashed_api_key = generate_api_key()
    api_keys[api_key] = {"user_id": user_id, "created_at": datetime.datetime.now()}
    # In a real application, store this in a database.
    # db.session.add(ApiKey(api_key=hashed_api_key, user_id=user_id))
    # db.session.commit()
    return api_key


def revoke_api_key(api_key):
    """Revokes an API key."""
    if api_key in api_keys:
        del api_keys[api_key]
        # In a real application, update the database record.
        # api_key_record = db.session.query(ApiKey).filter_by(api_key=api_key).first()
        # if api_key_record:
        #     api_key_record.revoked = True
        #     db.session.commit()
        return True
    return False


def rotate_api_key(api_key):
    """Rotates an API key."""
    if api_key in api_keys:
        user_id = api_keys[api_key]["user_id"]
        new_api_key, hashed_new_api_key = generate_api_key()
        
        # Update in-memory storage
        del api_keys[api_key]
        api_keys[new_api_key] = {"user_id": user_id, "created_at": datetime.datetime.now()}
        
        # In a real application, update the database record and potentially invalidate the old key.
        # api_key_record = db.session.query(ApiKey).filter_by(api_key=api_key).first()
        # if api_key_record:
        #     api_key_record.revoked = True
        #     db.session.add(ApiKey(api_key=hashed_new_api_key, user_id=user_id))
        #     db.session.commit()
        return new_api_key
    return None


def authenticate_api_key(api_key):
    """Authenticates an API key."""
    if api_key in api_keys:
        return api_keys[api_key]["user_id"]
    return None


def requires_api_key(f):
    """Decorator to require an API key for a route."""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return jsonify({"message": "API key missing"}), 401

        user_id = authenticate_api_key(api_key)
        if not user_id:
            return jsonify({"message": "Invalid API key"}), 401

        # In a real application, you might perform additional authorization checks here.
        # For example, check if the user has permission to access this specific resource.

        return f(*args, **kwargs, user_id=user_id)
    return decorated

# Example API endpoint protected by API key
@app.route("/protected", methods=["GET"])
@requires_api_key
def protected_endpoint(user_id):
    """An example API endpoint that requires an API key."""
    return jsonify({"message": "This is a protected endpoint.", "user_id": user_id}), 200

# API key management endpoints (for testing/admin purposes - secure appropriately)
@app.route("/api_keys", methods=["POST"])
def create_key():
    """Creates a new API key (for testing/admin purposes)."""
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400
    
    api_key = create_api_key(user_id)
    return jsonify({"api_key": api_key}), 201

@app.route("/api_keys/<string:api_key>", methods=["DELETE"])
def delete_key(api_key):
    """Revokes an API key (for testing/admin purposes)."""
    if revoke_api_key(api_key):
        return jsonify({"message": "API key revoked"}), 200
    else:
        return jsonify({"message": "API key not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)