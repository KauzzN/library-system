import secrets

from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify, session
from flask_mail import Message

import bcrypt

from app.extensions.mail import mail
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

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    
    data = request.get_json()
    
    email = data.get("email")
    
    query_user = """
        SELECT * FROM users
        WHERE email = ?;
    """
    
    cursor.execute(query_user, (email,))
    
    user = cursor.fetchone()
    
    if not user:
        return jsonify({
            "error": "Usuário não encontrado"
        }), 404
    
    token = secrets.token_urlsafe(32)
    
    expires_at = (
        datetime.now() + timedelta(minutes=30)
    )
    
    query_insert = """
        INSERT INTO password_resets(user_id, token, expires_at)
        VALUES (?, ?, ?);
    """
    
    values = (user["id"], token, expires_at)
    cursor.execute(query_insert, values)
    
    connection.commit()
    
    reset_link = (
        f"http://localhost:5000//validade-reset-token/{token}"
    )
    
    msg = Message(
        subject="Recuperação de senha",
        recipients=[email]
    )
    
    msg.body = f"""
        Olá!
        
        Recebemos uma solicitação para redefinir sua senha.
        
        Clique no link abaixo:
        
        {reset_link}
        
        Este link expira em 30 minutos.
        
        Caso não tenha solicitado a alteração,
        ignore este email.
    """
    
    mail.send(msg)
    
    return jsonify({
        "message": "Email enviado com sucesso"
    }), 200
    
    
@auth_bp.route("/validade-reset-token/<token>", methods=["GET"])
def validade_reset_token(token):
    query = """
        SELECT * FROM password_resets
        WHERE token = ?
        AND used = 0
    """
    
    cursor.execute(query, (token,))
    
    reset = cursor.fetchone()
    
    if not reset:
        return jsonify({
            "error": "Token inválido"
        }), 400
        
    expires_at = datetime.fromisoformat(
        reset["expires_at"]
    )
    
    if datetime.now() > expires_at:
        return jsonify({
            "error": "link expirado"
        }), 400
        
    return jsonify({
        "valid": True
    }), 200
    

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    
    data = request.get_json()
    
    token = data.get("token")
    
    new_password = data.get(
        "new_password"
    )
    
    query_token  = """
        SELECT * FROM password_resets
        WHERE token = ?
        AND used = 0;
    """
    
    cursor.execute(query_token, (token,))
    
    reset = cursor.fetchone()
    
    if not reset:
        return jsonify({
            "error": "Token inválido"
        }), 400
        
    expires_at = datetime.fromisoformat(
        reset["expires_at"]
    )
    
    if datetime.now() > expires_at:
        return jsonify({
            "error": "link expirado"
        }), 400
        
    password_hash = bcrypt.hashpw(
        new_password.encode("utf-8"),
        bcrypt.gensalt()
    )
    
    query_update = """
        UPDATE users
        SET password = ?
        WHERE id = ?;
    """
    
    cursor.execute(query_update, (password_hash.decode("utf-8"), reset["user_id"]))
    
    query_used = """
        UPDATE password_resets
        SET used = 1
        WHERE id = ?;
    """
    
    cursor.execute(query_used, (reset["id"],))

    connection.commit()
    
    return jsonify({
        "message": "Senha alterada com sucesso"
    }), 200
    
    
    