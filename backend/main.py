from flask import Flask
from flask_jwt_extended import JWTManager

from app.config.config import Config

from app.routes.auth_routes import auth_bp
from app.routes.book_routes import books_hp
from app.routes.category_routes import categories_bp
from app.routes.loan_routes import loans_hp

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(books_hp)
app.register_blueprint(categories_bp)
app.register_blueprint(loans_hp)

@app.route("/")
def home():
    return {
        "message": "API funcionando"
    }

if __name__ == "__main__":
    app.run(debug=True)