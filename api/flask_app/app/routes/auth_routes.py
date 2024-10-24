from flask import Blueprint, request, jsonify, session
from app.models.user import User
from app.utils.helpers import generate_user_id
from flask_login import login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    from app import db, bcrypt  # Import inside the function to avoid circular import
    data = request.get_json()
    user = User.query.filter_by(login_id=data['login_id']).first()

    if user and user.check_password(data['password']):
        login_user(user)
        session['user_id'] = user.user_id
        session.permanent = True
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out!"}), 200

@auth_bp.route('/menu', methods=['GET'])
def menu():
    if 'user_id' in session:
        return jsonify({"message": "Welcome to the Menu!"}), 200
    return jsonify({"message": "You are not logged in!"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    from app import db, bcrypt  # Import inside the function to avoid circular import
    data = request.get_json()
    user_id = generate_user_id()
    user = User(user_id=user_id, login_id=data['login_id'], user_name=data['user_name'], email=data['email'], role_id=data['role_id'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!", "user_id": user_id}), 201
