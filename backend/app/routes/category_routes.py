from flask import Blueprint, request, jsonify, session

from app.database.connection import cursor, connection

categories_bp = Blueprint(
    "categories",
    __name__,
    url_prefix="/categories"
)

@categories_bp.route("/create", methods=["POST"])
def create_category():
    
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({
            "error": "não autenticado"
        }), 401
    
    data = request.get_json()
    
    name = data.get("name")
    description = data.get("description")

    query = """
        INSERT INTO categories(
            user_id,
            name,
            description
        )
        
        VALUES (?, ?, ?)
    """
    
    values = (user_id, name, description)
    
    cursor.execute(query, values)
    
    connection.commit()
    
    return jsonify({
        "message": "Categoria criada com successo",
        
        "category": {
            "name": name,
            "description": description,
            "user_id": user_id
        }
    }),201
    
@categories_bp.route("/", methods=["GET"])
def read_categorys():
    
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({
            "error": "não autenticado"
        }), 401
    
    query = """
        SELECT * FROM categories
        WHERE user_id = ?
    """
    
    cursor.execute(query, (user_id,))
    
    categories = cursor.fetchall()
    
    if not categories:
        return jsonify({
            "error": "nenhuma categoria encontrada"
        }), 404
    
    categories_list = []
    
    for category in categories:
        
        categories_list.append({
            "id": category["id"],
            "name": category["name"],
            "description": category["description"]
        })
    
    return jsonify({"categories": categories_list}), 200
        
@categories_bp.route("<int:category_id>", methods=["GET"])
def get_category(category_id):
    
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({
            "error": "não autenticado"
        }), 401
    
    query = """
        SELECT * FROM categories
        WHERE id = ?
        AND user_id = ?;
    """
    
    cursor.execute(query, (category_id, user_id))
    category = cursor.fetchone()
    
    if not category:
        return jsonify({
            "error": "Categoria não encontrada"
        }), 404
        
    return jsonify({
        "Category": {
            "id": category["id"],
            "name": category["name"],
            "description": category["description"],
            "user_id": category["user_id"]
        }
    })
    
@categories_bp.route("/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "não autenticado"
        }), 401
        
    data = request.get_json()
    
    name = data.get("name")
    description = data.get("description")
    
    query = """
        UPDATE categories
        SET 
            name = ?,
            description = ?
        WHERE id = ?
        AND user_id = ?;
    """
    
    cursor.execute(query, (name, description, category_id, user_id))
    
    connection.commit()
    
    return jsonify({
        "message": "categoria atualizada com sucesso"
    }), 201
    
@categories_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({
            "error": "não autenticado"
        }), 401
        
    query = """
        DELETE FROM categories
        WHERE id = ?
        AND user_id = ?;
    """
    
    cursor.execute(query, (category_id, user_id))
    
    connection.commit()
    
    return jsonify({
        "message": "categoria deletada com sucesso"
    }), 201
    
    
    
    