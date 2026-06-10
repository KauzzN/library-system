
import random
from flask import Blueprint, request, jsonify, session
import pymysql
from flask_mail import Mail, Message
from app.extensions.mail import mail

codigo_recuperado_gerado = None

def conectaDB():
    db = pymysql.connect(
        host='localhost',
        database='bibliotecadb',
        user='root',
        passwd='admin'
    )
    return db

auth_bp = Blueprint(
    "auth",
    __name__, 
    url_prefix="/auth"
)

# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    banco = None
    try:
        data = request.get_json()
        email = data.get("email")
        senha = data.get("senha")

        banco = conectaDB()
        cursor = banco.cursor()

        sql = f"Call Login('{email}', '{senha}');"
        cursor.execute(sql)

        resultado = cursor.fetchone()
        if resultado:
            response = {"message": "Login realizado com sucesso", "codigo": 200, 
                        "gerente": {"email": resultado[1], "senha": resultado[2]}}
            session["user_id"] = resultado[0]
        else:
            response = {"error": "Email ou senha incorretos", "codigo": 401}
    except Exception as e:
        print("Erro ao realizar login:", e)
        response = {"error": "Falha ao realizar login", "codigo": 401, "erro": str(e)}
    finally:
        if banco is not None:
            banco.close()
    return jsonify(response)

@auth_bp.route("/logout", methods=["POST"])
def logout():
    
    session.clear()
    
    return jsonify({
        "message": "Logout realizado com sucesso"}), 200
    
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    banco = None
    try:
        data = request.get_json()
        email = data.get("email")

        banco = conectaDB()
        cursor = banco.cursor()
        sql = f"Call RecuperarSenha('{email}');"
        cursor.execute(sql)

        resultado = cursor.fetchone()
        if resultado:
            msg = Message("Recuperação de senha", sender="biblioteca.ex.ads@gmail.com", recipients=[email])
            global codigo_recuperado_gerado
            codigo_recuperado_gerado = random.randint(100000, 999999)
            msg.body = f"Olá, {resultado[0]}! Use o seguinte código para recuperar sua senha: {codigo_recuperado_gerado}"
            mail.send(msg)

            response = {"message": "Código de recuperação enviado para o email", "codigo": 200, 
                        "Gerente": {"id": resultado[0], "login": resultado[1], "email": resultado[2]}}
        else:
            response = {"error": "Email não encontrado", "codigo": 404}
    except Exception as e:
        print("Erro ao enviar email de recuperação:", e)
        response = {"error": "Falha ao enviar email de recuperação", "codigo": 400, "erro": str(e)}
    finally:
        if banco is not None:
            banco.close()

    return jsonify(response)

@auth_bp.route("/reset-password", methods=["PUT"])
def reset_password():
    global codigo_recuperado_gerado
    banco = None
    try:
        data = request.get_json()
        email = data.get("email")
        codigo_recuperacao_recebido = data.get("codigoRecuperacao")
        nova_senha = data.get("novaSenha")
        
        print(f"Codigo recebido: {codigo_recuperacao_recebido}, Codigo gerado: {codigo_recuperado_gerado}")

        codigo_recuperacao_recebido = int(codigo_recuperacao_recebido)
        if codigo_recuperado_gerado is None or codigo_recuperacao_recebido != codigo_recuperado_gerado:
            return jsonify({"error": "Codigo de recuperação invalido", "codigo": 400})
        
        banco = conectaDB()
        cursor = banco.cursor()

        # Use CALL with parameterized query to avoid SQL syntax errors and injection
        sql = "CALL AtualizarSenha(%s, %s);"
        cursor.execute(sql, (nova_senha, email))
        banco.commit()

        response = {"message": "Senha atualizada com sucesso", "codigo": 200}
    except Exception as e:
        print("Erro ao atualizar senha:", e)
        response = {"error": "Falha ao atualizar senha", "codigo": 400, "erro": str(e)}
    finally:
        if banco is not None:
            banco.close()
    return jsonify(response)
    
    
    