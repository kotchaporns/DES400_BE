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

def getpredict(user_id, date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()

        result = Record.query.filter_by(user_id=user_id, date=date).all()

        if result:
            print(result) 
        else:
            print("No records found")

        records = [{'record_id': entry.record_id, 'user_id': entry.user_id,
                    'date': entry.date.strftime('%Y-%m-%d'),
                    'time_start': entry.time_start.strftime('%H:%M:%S'),
                    'time_stop': entry.time_stop.strftime('%H:%M:%S'),
                    'path': entry.path, 
                    'calls': entry.calls,
                    'model_result': entry.model_result} for entry in result]

        return {"response": records}

    except Exception as e:
        return {"error": 'Invalid input'}
    
