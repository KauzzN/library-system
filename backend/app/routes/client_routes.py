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

client_hp = Blueprint(
    "client", 
    __name__,
    url_prefix="/client"
)

@client_hp.route("/create", methods=["POST"])
def create_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Não autenticado"}), 401
        
    getdata = request.get_json()
    nome = getdata["nome"]
    cpf = getdata["cpf"]
    telefone = getdata["telefone"]
    endereco = getdata["endereco"]

    try:
        banco = conectaDB()
        cursor = banco.cursor()

        sql = f"Call InsertCliente('{nome}', '{cpf}', '{telefone}', '{endereco}');"
        cursor.execute(sql)
        banco.commit()
       
        response = {"mensagem" : "Cliente cadastrado com sucesso", "codigo" : 200} 
    except Exception as e:
        print("Erro ao cadastrar cliente: ", e)
        response = {"error": "Falha ao cadastrar cliente"}
    finally:
        banco.close()

    return jsonify(response)

@client_hp.route("/list", methods=["GET"])
def read_clients():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Não autenticado"}), 401

    try:
        banco = conectaDB()
        cursor = banco.cursor()
        sql = "CALL GetClientes();"
        cursor.execute(sql)
        resultado = cursor.fetchall()

        clientes = []
        for cliente in resultado:
            clientes.append({
                "id": cliente[0],
                "nome": cliente[1],
                "cpf": cliente[2],
                "telefone": cliente[3],
                "endereco": cliente[4]
            })
    finally:
        banco.close()

    return jsonify(clientes)