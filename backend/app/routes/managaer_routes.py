from flask import Blueprint, jsonify, request
import pymysql


def conectaDB():
    db = pymysql.connect(
        host='localhost',
        database='bibliotecadb',
        user='root',
        passwd='admin'
    )
    return db

manager_bp = Blueprint(
    "manager",
    __name__, 
    url_prefix="/manager"
)

# Register
@manager_bp.route("/create", methods=["POST"])
def register_account():
    getdata = request.get_json()
    login = getdata["login"]
    senha = getdata["senha"]
    email = getdata["email"]

    try:
        banco = conectaDB()
        cursor = banco.cursor()

        sql = f"Call InsertGerente('{login}', '{senha}', '{email}');"
        cursor.execute(sql)
        banco.commit()
        response = {"mensagem": "Cadastrado com sucesso", "codigo": 200}
    except Exception as e:
        print("Erro ao cadastrar gerente:", e)
        response = {"mensagem": "Erro ao cadastrar gerente", "codigo": 500, "erro": str(e)}
    finally:
        if banco:
            banco.close()

    return jsonify(response)