from flask import Blueprint, request, jsonify, session

from app.database.connection import connection, cursor

loans_hp = Blueprint(
    "loans", 
    __name__,
    url_prefix="/loans"
)

@loans_hp.route("/create", methods=["POST"])
def create_loan():
    
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({
            "error": "não autenticado"
        }), 401
        
    data = request.get_json()
    
    book_id = data.get("book_id")
    customer_name = data.get("customer_name")
    customer_phone = data.get("customer_phone")
    
    query_book = """
        SELECT * FROM books
        WHERE id = ?
        AND user_id = ?
    """
    
    cursor.execute(query_book, (book_id, user_id))
    
    book = cursor.fetchone()
    
    if not book:
        return jsonify({
            "error": "livro não encontrado"
        }), 404
        
        
    if book["quantity"] <= 0:
        return jsonify({
            "error": "livro sem estoque"
        }), 400
        
    query_loan = """
        INSERT INTO loans(
            user_id,
            book_id,
            customer_name,
            customer_phone
        )
        VALUES (?, ?, ?, ?)
    """
    
    values = (user_id, book_id, customer_name, customer_phone)
    
    cursor.execute(query_loan, values)
    
    query_update_book = """
        UPDATE books
        SET quantity = quantity - 1
        WHERE id = ?
    """
    
    cursor.execute(query_update_book, (book_id,))
    
    connection.commit()
    
    return jsonify({
        "message": "emprestimo realizado com sucesso"
    })
        
@loans_hp.route("/", methods=["GET"])
def read_loans(): 
    
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({
            "error": "não autenticado"
        }), 401
    
    query = """
        SELECT
            loans.id,
            books.title,
            loans.customer_name,
            loans.customer_phone,
            loans.status,
            loans.loan_date,
            loans.return_date
        FROM loans
            INNER JOIN books
                ON loans.book_id = books.id
        WHERE loans.user_id = ?
    """
    
    cursor.execute(query, (user_id,))
    
    loans = cursor.fetchall()
    
    if not loans:
        return jsonify({
            "error": "emprestimos não encontrados"
        }), 404

    loans_list = []
    
    for loan in loans:
   
        loans_list.append({
            "id": loan["id"],
            "book_title": loan["title"],
            "customer_name": loan["customer_name"],
            "customer_phone": loan["customer_phone"],
            "status": loan["status"],
            "loan_date": loan["loan_date"],
            "return_date": loan["return_date"]
        })
   
    return jsonify({"emprestimos": loans_list}), 200
        
@loans_hp.route("/<int:loans_id>/return", methods=["POST"])
def return_loan(loans_id):
    
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({
            "error": "não autenticado"
        }), 401
        
    query_loan = """
        SELECT * FROM loans
        WHERE id = ?
        AND user_id = ?
    """
    
    cursor.execute(query_loan, (loans_id, user_id,))
    
    loan = cursor.fetchone()
    
    if not loan:
        return jsonify({
            "error": "emprestimo não encontrado"
        }), 404
    
    
    if loan["status"] == "returned":
        return jsonify({
            "error": "livro já devolvido"
        }), 400
        
    query_update_loan = """
        UPDATE loans
        SET
            status = 'returned',
            return_date = CURRENT_TIMESTAMP
        WHERE id = ?;
    """
    
    cursor.execute(query_update_loan, (loans_id,))
    
    query_update_book = """
        UPDATE books
        SET quantity = quantity + 1
        WHERE id = ?;
    """
    
    query_find_book = """
        SELECT book_id FROM loans
        WHERE id = ?
    """
    
    cursor.execute(query_find_book, (loans_id,))
    book_id = cursor.fetchone()
    
    cursor.execute(query_update_book, (book_id["book_id"],))
    connection.commit()
    
    return jsonify({
        "message": "livro devolvido com sucesso"
    }), 200
    
    