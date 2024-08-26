from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_session import Session
from datetime import timedelta, datetime

app = Flask(__name__)
CORS(app)

# アプリケーション設定
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root2997@localhost/Resell'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
Session(app)

# ユーザーモデルの定義
class user_info(db.Model):
    user_id = db.Column(db.String(6), primary_key=True)
    login_id = db.Column(db.String(255), unique=True, nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
# ID生成ロジック
def generate_user_id():
    last_user = user_info.query.order_by(user_info.user_id.desc()).first()
    if last_user:
        new_id = str(int(last_user.user_id) + 1).zfill(6)
    else:
        new_id = '000001'
    return new_id

# データベースの初期化
with app.app_context():
    db.create_all()

    # ログインAPI
@app.route('/test', methods=['POST'])
def test():
    data = request.get_json()
    user_id = generate_user_id()
    user = user_info(user_id=user_id, login_id=data['login_id'], user_name=data['user_name'], email=data['email'], role_id=data['role_id'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!", "user_id": user_id}), 201


# ログインAPI
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = user_info.query.filter_by(login_id=data['login_id']).first()
    
    if user and user.check_password(data['password']):
        session['user_id'] = user.user_id
        session.permanent = True
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

# ログアウトAPI
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out!"}), 200

# 認証が必要な保護されたルート
@app.route('/protected', methods=['GET'])
def protected():
    if 'user_id' in session:
        return jsonify({"message": "This is a protected route."}), 200
    return jsonify({"message": "You are not logged in!"}), 401

if __name__ == '__main__':
    app.run(debug=True)
