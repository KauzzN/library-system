from flask import Blueprint, request, jsonify, session
import pymysql

def conectaDB():
    db = pymysql.connect(
        host='localhost',
        database='bibliotecadb',
        user='root',
        passwd='admin'
    )
    return db

loans_hp = Blueprint(
    "loans", 
    __name__,
    url_prefix="/loans"
)

@loans_hp.route("/create", methods=["POST"])
def create_loan():

    user_id = session.get("user_id")
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