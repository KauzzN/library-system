from flask import Blueprint, request, jsonify, session

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

    session["user_id"] = user["id"]

    return jsonify({
        "message": "Login realizado com sucesso",
        
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }), 200
    
@auth_bp.route("/logout", methods=["POST"])
def logout():
    
    session.clear()
    
    return jsonify({
        "message": "Logout realizado com sucesso"
    }), 200
    
@auth_bp.route("/me", methods=["GET"])
def me():
    
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({
            "error": "Não autenticado"
        }), 401
        
    query_user = """
        SELECT id, name, email
        FROM users
        WHERE id = ?;
    """
    
    cursor.execute(query_user, (user_id,))
    
    user = cursor.fetchone()
    
    return jsonify({
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        },
    }), 200

