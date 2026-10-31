from flask import Blueprint, request, jsonify
import uuid
import bcrypt
import json

roles_bp = Blueprint('roles', __name__)

# In-memory role storage (replace with database in production)
roles = {}

# Define roles and their permissions
ROLES = {
    "Administrator": ["read", "write", "delete", "admin"],
    "Editor": ["read", "write"],
    "Viewer": ["read"]
}


def validate_role_name(role_name):
    """Validates the role name."""
    if not isinstance(role_name, str) or not role_name:
        return False
    return True


@roles_bp.route('/roles', methods=['POST'])
def create_role():
    """Creates a new role."""
    data = request.get_json()
    role_name = data.get('name')
    permissions = data.get('permissions', [])

    if not validate_role_name(role_name):
        return jsonify({"error": "Invalid role name"}), 400

    if role_name in roles:
        return jsonify({"error": "Role already exists"}), 409

    roles[role_name] = {"permissions": permissions}
    return jsonify({"message": "Role created successfully"}), 201


@roles_bp.route('/roles/<role_name>', methods=['GET'])
def get_role(role_name):
    """Retrieves a role by name."""
    if role_name not in roles:
        return jsonify({"error": "Role not found"}), 404

    return jsonify(roles[role_name]), 200


@roles_bp.route('/roles/<role_name>', methods=['PUT'])
def update_role(role_name):
    """Updates a role."""
    data = request.get_json()
    permissions = data.get('permissions')

    if role_name not in roles:
        return jsonify({"error": "Role not found"}), 404

    if permissions is not None:
        roles[role_name]["permissions"] = permissions

    return jsonify({"message": "Role updated successfully"}), 200


@roles_bp.route('/roles/<role_name>', methods=['DELETE'])
def delete_role(role_name):
    """Deletes a role."""
    if role_name not in roles:
        return jsonify({"error": "Role not found"}), 404

    del roles[role_name]
    return jsonify({"message": "Role deleted successfully"}), 200


@roles_bp.route('/users/register', methods=['POST'])
def register_user():
    """Registers a new user with a role."""
    data = request.get_json()
    role = data.get('role')
    email = data.get('email')
    password = data.get('password')

    if not role or not email or not password:
        return jsonify({"error": "Missing parameters"}), 400

    if not validate_role_name(role):
        return jsonify({"error": "Invalid role name"}), 400

    if email in [user['email'] for user in users.values()]:
        return jsonify({"error": "Email already exists"}), 409

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create a new user
    user_id = str(uuid.uuid4())
    users[user_id] = {
        "role": role,
        "email": email,
        "password": hashed_password.decode('utf-8')
    }

    # Generate a token (replace with a more robust token generation mechanism)
    token = str(uuid.uuid4())

    return jsonify({"id": user_id, "token": token}), 201


users = {} # In memory user store. Replace with database.