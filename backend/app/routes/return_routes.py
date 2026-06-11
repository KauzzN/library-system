from flask import Blueprint, request, jsonify, session
import pymysql

def conectaDB():
    db = pymysql.connect(
        host='localhost',
        database='library_system',
        user='root',
        passwd='120808'
    )
    return db

returns_bp = Blueprint(
    "returns", 
    __name__,
    url_prefix="/returns"
)

@returns_bp.route("/delete", methods=["POST"])
def return_loan():

        getdata = request.get_json()
        cpf = getdata.get("cpf")

        try:
            banco = conectaDB()
            cursor = banco.cursor()

            cursor.execute("CALL DeleteEmprestimo(%s);", (cpf,))
            banco.commit()

            response = {"mensagem": f"Empréstimo deletado com sucesso", "codigo": 200}
        except Exception as e:
            print("Erro ao deletar empréstimo:", e)
            response = {"error": str(e)}
        finally:
            if banco:
                banco.close()

        return jsonify(response)