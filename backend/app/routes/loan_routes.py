from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import (get_jwt_identity, jwt_required)
import pymysql

def conectaDB():
    db = pymysql.connect(
        host='localhost',
        database='library_system',
        user='root',
        passwd='120808'
    )
    return db

loans_hp = Blueprint(
    "loans", 
    __name__,
    url_prefix="/loans"
)

@loans_hp.route("/create", methods=["POST"])
@jwt_required()
def create_loan():

    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "Não autenticado"}), 401
        
    getdata = request.get_json()
    
    dias = getdata.get("dias")
    nome = getdata.get("nome")
    telefone = getdata.get("telefone")
    cpf = getdata.get("cpf")
    idlivro = getdata.get("idlivro")

    try:
        banco = conectaDB()
        cursor = banco.cursor()

        cursor.execute("CALL InsertEmprestimo(%s, %s, %s, %s, %s);", (dias, nome, telefone, cpf, idlivro))
        banco.commit()

        response = {"mensagem": f"Empréstimo cadastrado com sucesso", "codigo": 200}
    except Exception as e:
        print("Erro ao criar empréstimo:", e)
        response = {"error": str(e)}
    finally:
        if banco:
            banco.close()

    return jsonify(response)

@loans_hp.route("/read", methods=["GET"])
@jwt_required()
def read_loans():
    
    try:
        banco = conectaDB()
        cursor = banco.cursor(pymysql.cursors.DictCursor)
        
        sql = """
            SELECT
                e.idemprestimo,
                l.nome AS livro,
                e.nome,
                e.telefone,
                e.cpf,
                e.qtd_dias
            FROM emprestimo e
            INNER JOIN livro l
                ON e.fk_idlivro = l.idlivro;
        """

        cursor.execute(sql)
        
        loans = cursor.fetchall()
        
        return jsonify(loans), 200
    
    except Exception as e:
        
        print("Erro ao listar emprestimos:", e)
        
        return jsonify({
            "error": str(e)
        }), 500
        
    finally:
        if banco:
            banco.close()
        