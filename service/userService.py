from werkzeug.security import generate_password_hash, check_password_hash
from entity.userEntity import db, User
from flask_bcrypt import Bcrypt
from entity.recordEntity import Record
from datetime import datetime


bcrypt = Bcrypt()

def create_user(username, email, password, gender, birthday, firstname, lastname, weight, height, medical_condition, nationality):
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=password, gender=gender, birthday=birthday, firstname=firstname, lastname=lastname, weight=weight, height=height, medical_condition=medical_condition, nationality=nationality)
    db.session.add(user)
    db.session.commit()
    return user

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if bcrypt.check_password_hash(user.password,password):
            return {'mesage':'Login successful', 'user_id': user.user_id, 'username': user.username}
        else:
            return {"error": 'Invalid password'}
    else:
        return {"error": 'Invalid email'}
    
def getuser(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user_id:
        return {'mesage':'Login successful', 'user_id': user.user_id, 'username': user.username, 'email': user.email,'gender': user.gender, 'birthday': user.birthday, 'firstname': user.firstname, 'lastname': user.lastname, 'weight': user.weight, 'height': user.height, 'medical_condition': user.medical_condition, 'nationality': user.nationality}
    else:
        return {"error": 'Invalid user_id'}

def updateUser(user_id, data):
        try:
            user = User.query.get(user_id)
            if not user:
                return {'error': 'User not found'}

            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.password = data.get('password', user.password)
            user.gender = data.get('gender', user.gender)
            user.birthday = data.get('birthday', user.birthday)
            user.firstname = data.get('firstname', user.firstname)
            user.lastname = data.get('lastname', user.lastname)
            user.weight = data.get('weight', user.weight)
            user.height = data.get('height', user.height)
            user.medical_condition = data.get('medical_condition', user.medical_condition)
            user.nationality = data.get('nationality', user.nationality)

            db.session.commit()

            return {
                'success': 'Update user successfully',
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'gender': user.gender,
                'birthday': user.birthday,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'weight': user.weight,
                'height': user.height,
                'medical_condition': user.medical_condition,
                'nationality': user.nationality
            }

        except Exception as e:
            return {"Error update user": f"{e}"}
    
