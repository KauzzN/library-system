
import random
from flask import Blueprint, request, jsonify, session
import pymysql
from flask_mail import Mail, Message
from app.extensions.mail import mail
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

codigos_recuperacao = {}

def conectaDB():
    db = pymysql.connect(
        host='localhost',
        database='library_system',
        user='root',
        passwd='120808'
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
            access_token = create_access_token(
                identity=str(resultado[0])
            )
            response = {"message": "Login realizado com sucesso", "codigo": 200, 
                        "token": access_token,
                        "gerente": {"email": resultado[1]}}
        else:
            response = {"error": "Email ou senha incorretos", "codigo": 401}
    except Exception as e:
        print("Erro ao realizar login:", e)
        response = {"error": "Falha ao realizar login", "codigo": 401, "erro": str(e)}
    finally:
        if banco is not None:
            banco.close()
    return jsonify(response)
    
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
            codigo = random.randint(100000, 999999)
            
            codigos_recuperacao[email] = codigo
            msg.body = f"Olá, {resultado[1]}! Use o seguinte código para recuperar sua senha: {codigo}"
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
    banco = None
    try:
        data = request.get_json()
        email = data.get("email")
        codigo_recuperacao_recebido = int(data.get("codigoRecuperacao"))
        nova_senha = data.get("novaSenha")
        
        codigo_salvo = codigos_recuperacao.get(email)
        
        if codigo_salvo is None:
            return jsonify({
                "error": "nenhum código foi solicitado para este email"
            }), 400

        if codigo_recuperacao_recebido != codigo_salvo:
            return jsonify({
                "error": "código inválido"
            }), 400
        
        banco = conectaDB()
        cursor = banco.cursor()

        # Use CALL with parameterized query to avoid SQL syntax errors and injection
        sql = "CALL AtualizarSenha(%s, %s);"
        cursor.execute(sql, (nova_senha, email))
        banco.commit()

        codigos_recuperacao.pop(email, None)
        response = {"message": "Senha atualizada com sucesso", "codigo": 200}
    except Exception as e:
        print("Erro ao atualizar senha:", e)
        response = {"error": "Falha ao atualizar senha", "codigo": 400, "erro": str(e)}
    finally:
        if banco is not None:
            banco.close()
    return jsonify(response)
    
    
    