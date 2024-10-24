from app.models.user import User
from app import bcrypt

def generate_user_id():
    last_user = User.query.order_by(User.user_id.desc()).first()
    if last_user:
        new_id = str(int(last_user.user_id) + 1).zfill(6)
    else:
        new_id = '000001'
    return new_id

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')
