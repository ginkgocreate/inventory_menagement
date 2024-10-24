from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
session = Session()

def create_app():
    app = Flask(__name__)
    app.secret_key = '299792458#'
    app.config.from_object(Config)

    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    db.init_app(app)
    bcrypt.init_app(app)
    session.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(user_id)

    with app.app_context():
        from app.routes.auth_routes import auth_bp
        from app.routes.procurement_routes import procurement_bp
        from app.routes.stock_routes import stock_bp
        from app.routes.sales_routes import sales_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(procurement_bp, url_prefix='/procurement')
        app.register_blueprint(stock_bp, url_prefix='/stock')
        app.register_blueprint(sales_bp, url_prefix='/sales')

    return app
