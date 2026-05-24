from flask import Flask
from flask_jwt_extended import JWTManager

from app.config.config import Config

from app.routes.auth_routes import auth_bp

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return {
        "message": "API funcionando"
    }

if __name__ == "__main__":
    app.run(debug=True)