from flask import Blueprint,request,jsonify
from service.userService import create_user, login, getpredict, getuser
from entity.userEntity import db, User

userController = Blueprint('userController', __name__)

@userController.route('/create-user', methods=['POST'])
def createUser():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        gender = data.get('gender')
        birthday = data.get('birthday')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        weight = data.get('weight')
        height = data.get('height')
        medical_condition = data.get('medical_condition')
        nationality = data.get('nationality')

        if not username or not email or not password:
            return jsonify({'error':'username, email, and password are required'}), 400
        
        user = create_user(username, email, password, gender, birthday, firstname, lastname, weight, height, medical_condition, nationality)
        print(user)
        
        return jsonify({'success': 'Create user successfully', 'user_id': user.user_id, 'username':user.username, 'email':user.email, 'gender':user.gender, 'birthday':user.birthday, 'firstname':user.firstname, 'lastname':user.lastname, 'weight':user.weight, 'height':user.height, 'medical_condition':user.medical_condition, 'nationality':user.nationality })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@userController.route('/login', methods=['POST'])
def userLogin():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error':'username, and password are required'}), 400
        
        result = login(username, password)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@userController.route('/getuser', methods=['POST'])
def userdata():
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({'error':'user_id are required'}), 400
        
        result = getuser(user_id)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@userController.route('/getpredict', methods=['POST'])
def userpredict():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        date = data.get('date')

        if not user_id or not date:
            return jsonify({'error':'user_id, and date are required'}), 400
        
        result = getpredict(user_id, date)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@userController.route('/update-user/<int:user_id>', methods=['PUT'])
def userupdate(user_id):
    try:
        data = request.get_json()
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

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

        return jsonify({
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
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


