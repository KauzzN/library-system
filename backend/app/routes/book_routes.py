from flask import Blueprint, request, jsonify
from flask_jwt_extended import(
    jwt_required,
    get_jwt_identity
)
import pymysql

def conectaDB():
    db = pymysql.connect(
        host='localhost',
        database='library_system',
        user='root',
        passwd='120808'
    )
    return db

books_hp = Blueprint(
    "books",
    __name__, 
    url_prefix="/books"
)

@books_hp.route("/list", methods=["GET"])
@jwt_required()
def read_books():
    listaLivros = []

    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "Não autenticado"}), 401
    
    try:
        banco = conectaDB()
        cursor = banco.cursor()

        sql = "Call GetLivros();"
        cursor.execute(sql)
        resultado = cursor.fetchall()

        for livro in resultado:
            listaLivros.append(
                {
                    "id": livro[0],
                    "nome": livro[1],
                    "categoria": livro[2],
                    "status": livro[3],
                    "estoque": livro[4]
                }
            )
    except Exception as e:
        print("Erro ao consultar livros:", e)
        return jsonify({"error": "Falha ao listar livros"}), 500
    finally:
            banco.close()

    return jsonify(listaLivros)


@books_hp.route("/create", methods=["POST"])
@jwt_required()
def create_book():

    banco = None

    try:
        user_id = get_jwt_identity()

        getdata = request.get_json()
        if not getdata:
            return jsonify({"error": "JSON inválido ou vazio"}), 400

        livros = getdata if isinstance(getdata, list) else [getdata]
        
        banco = conectaDB()
        cursor = banco.cursor()

        for livro in livros:
            
            nome = livro.get("nome")
            categoria = livro.get("categoria")
            status = livro.get("status")
            estoque = livro.get("estoque")

            if nome is None or categoria is None or status is None or estoque is None:
                return jsonify({"error": "Campos obrigatórios faltando"}), 400

            sql = "CALL InsertLivro(%s, %s, %s, %s);"
            cursor.execute(sql, (nome, categoria, status, estoque))

        banco.commit()
        return jsonify({
            "message": "Cadastrado com sucesso"
        }), 200
    except Exception as e:
        
        print("Erro ao cadastrar livro:", e)
        
        return jsonify({
            "error": "Erro ao cadastrar livro"
        }, 500)
    finally:
        if banco is not None:
            banco.close()

@books_hp.route("/update/<int:book_id>", methods=["PUT"])
@jwt_required()
def update_book(book_id):
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "Não autenticado"}), 401

    getdata = request.get_json()
    nome = getdata["nome"]
    categoria = getdata["categoria"]
    status = getdata["status"]
    estoque = getdata["estoque"]

    try:
        banco = conectaDB()
        cursor = banco.cursor()

        sql = "CALL AtualizarLivro(%s, %s, %s, %s, %s);"
        cursor.execute(sql, (book_id, nome, categoria, status, estoque))
        banco.commit()

        response = {"mensagem": "Atualizado com sucesso", "codigo": 200}
    except Exception as e:
        print("Erro ao atualizar livro:", e)
        response = {"mensagem": "Erro ao atualizar livro", "codigo": 500, "erro": str(e)}
        return jsonify(response), 500
    finally:
        banco.close()

    return jsonify(response)

@books_hp.route("/delete/<int:book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "Não autenticado"}), 401

    try:
        banco = conectaDB()
        cursor = banco.cursor()

        sql = "CALL DeleteLivro(%s);"
        cursor.execute(sql, (book_id,))
        banco.commit()

        response = {"mensagem": "Deletado com sucesso", "codigo": 200}
    except Exception as e:
        if "foreign key constraint fails" in str(e):
            return jsonify({
                "error": "Existem empréstimos vinculados a este livro. Não foi possivel deletar"
            }), 400
        
        print("Erro ao deletar livro:", e)
        response = {"mensagem": "Erro ao deletar livro", "codigo": 500, "erro": str(e)}
        return jsonify(response), 500
    finally:
        banco.close()

    return jsonify(response)
