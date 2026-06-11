from flask import Flask
from app.extensions.mail import mail
from flask_jwt_extended import JWTManager
from app.routes.auth_routes import auth_bp
from app.routes.book_routes import books_hp
from app.routes.loan_routes import loans_hp
from app.routes.managaer_routes import manager_bp
from app.routes.return_routes import returns_bp


app = Flask(__name__)
app.secret_key = '123'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'biblioteca.ex.ads@gmail.com'
app.config['MAIL_PASSWORD'] = 'erhu jtfa upnu bmlv'
app.config['MAIL_DEFAULT_SENDER'] = 'biblioteca.ex.ads@gmail.com'
app.config["JWT_SECRET_KEY"] = "library_system_ads_2026_jwt_secret_key_super_secure"

jwt = JWTManager(app)
mail.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(books_hp)
app.register_blueprint(loans_hp)
app.register_blueprint(manager_bp)
app.register_blueprint(returns_bp)

@app.route("/")
def home():
    return {
        "message": "API funcionando"
    }

if __name__ == "__main__":
    app.run(debug=True)