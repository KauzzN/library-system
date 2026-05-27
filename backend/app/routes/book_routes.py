from flask import Blueprint, request, jsonify, session

from app.database.connection import connection, cursor

books_hp = Blueprint(
    "books",
    __name__, 
    url_prefix="/books"
)

@books_hp.route("/create", methods=["POST"])
def create_book():
    
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({
            "error": "Não autenticado"
        }), 401
        
    data = request.get_json()
    
    title = data.get("title")
    author = data.get("author")
    quantity = data.get("quantity")
    category_id = data.get("category_id")
    
    query_category = """
        SELECT * FROM categories
        WHERE id = ?
        AND user_id = ?
    """
    
    cursor.execute(query_category, (category_id, user_id))
    
    category = cursor.fetchone()
    
    if not category:
        return jsonify({
            "message": "Categoria inválida"
        }), 400
    
    query = """
        INSERT INTO books(
            user_id, category_id, title, author, quantity
        )
        VALUES (?, ?, ?, ?, ?)
    """
    
    values = (
        user_id, 
        category_id,
        title,
        author,
        quantity
    )
    
    cursor.execute(query, values)
    
    connection.commit()
    
    return jsonify({
        "message": "Livro cadastrado com sucesso"
    }), 201
    
@books_hp.route("/listar", methods=["GET"])
def read_books():

    user_id = session.get("user_id")
    
    query_books = """
        SELECT * FROM books
        WHERE user_id = ?;
    """
    
    cursor.execute(query_books, (user_id,))
    
    books = cursor.fetchall()
    
    if not books:
        return jsonify({
            "error": "nenhum livro cadastrado"
        }), 401
        
    books_list = []
    
    for book in books:
        
        books_list.append({
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "quantity": book["quantity"],
            "category_id": book["category_id"]
        })
        
    return jsonify({"books": books_list}), 200
        
@books_hp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({
            "error": "Não autenticado"
        }), 401
        
    query = """
        SELECT * FROM books
        WHERE id = ?
        AND user_id = ?;
    """
    
    cursor.execute(query, (
        book_id,
        user_id
    ))
    
    book = cursor.fetchone()
    
    if not book:
        return jsonify({
            "error": "livro não encontrado"
        }), 404
        
    return jsonify({
            "Book": {
                "title": book["title"],
                "author": book["author"],
                "quantity": book["quantity"],
                "category_id": book["category_id"]
            }
        })
    
@books_hp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({
            "error": "não autenticado"
        }), 401
        
    data = request.get_json()
    
    title = data.get("title")
    author = data.get("author")
    quantity = data.get("quantity")
    category = data.get("category_id")
    
    query = """
        UPDATE books
        SET 
            title = ?,
            author = ?,
            quantity = ?,
            category_id = ?
        WHERE id = ?
        AND user_id = ?;
    """
    
    values = (title, author, quantity, category, book_id, user_id)
    
    cursor.execute(query, values)
    
    connection.commit()
    
    return jsonify({
        "message": "Livro atualizado com sucesso"
    }), 201
    
@books_hp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):

    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({
            "error": "não autenticado"
        }), 401
        
    query = """
        DELETE FROM books
        WHERE id = ?
        AND user_id = ?
    """
    
    cursor.execute(query, (book_id, user_id))
    
    connection.commit()
    
    return jsonify({
        "message": "livro deletado com sucesso"
    }), 201
    
    