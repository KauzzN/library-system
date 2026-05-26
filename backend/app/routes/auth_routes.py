from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

import bcrypt

from app.database.connection import connection, cursor

auth_bp = Blueprint("auth", __name__)


# Register
@auth_bp.route("/register", methods=["POST"])
def register_account():
    
    data = request.get_json()
    
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    query_user = """
        SELECT * FROM users
        WHERE email = ?;
    """
    
    cursor.execute(query_user, (email,))
    
    user_exists = cursor.fetchone()
    
    if user_exists:
        return jsonify({
            "error": "Usuário já existe"
        }), 409
        
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )
    
    query_insert = """
        INSERT INTO users(name, email, password)
        VALUES (?, ?, ?)
    """
    
    values = (
        username,
        email,
        password_hash.decode("utf-8")
    )
    
    cursor.execute(query_insert, values)
    
    connection.commit()
    
    return jsonify({
        "message": "Usuário criado com sucesso"
    }), 201
    


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    query_user = """
        SELECT * FROM users
        WHERE email = ?;
    """

    cursor.execute(query_user, (email,))

    user = cursor.fetchone()

    if not user:
        return jsonify({
            "error": "Credenciais inválidas"
        }), 401

    password_correct = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"].encode("utf-8")
    )

    if not password_correct:
        return jsonify({
            "error": "Credenciais inválidas"
        }), 401

    access_token = create_access_token(
        identity=user["id"]
    )

    return jsonify({
        "token": access_token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }), 200
