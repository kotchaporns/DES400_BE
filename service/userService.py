from werkzeug.security import generate_password_hash, check_password_hash
from entity.userEntity import db, User
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

def create_user(username, email, password):
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def login(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        if bcrypt.check_password_hash(user.password,password):
            return {'mesage':'Login successful', 'user_id': user.user_id, 'username': user.username, 'email':user.email}
        else:
            return {"error": 'Invalid password'}
    else:
        return {"error": 'Invalid email'}
