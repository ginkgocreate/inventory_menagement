# app/routes/__init__.py

from flask import Blueprint

# 個別のルートモジュールをインポート
from .auth_routes import auth_bp
from .procurement_routes import procurement_bp

# ルート用のメインブループリントを作成
main_bp = Blueprint('main', __name__)

# 個別のブループリントをメインブループリントに登録
main_bp.register_blueprint(auth_bp, url_prefix='/auth')
main_bp.register_blueprint(procurement_bp, url_prefix='/procurement')

# 共通のルートを定義、エラーハンドリングやランディングページにも使える
@main_bp.route('/')
def index():
    return "Welcome to the API"

# この main_bp は、アプリのファクトリ関数で登録されます
