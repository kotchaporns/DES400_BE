from flask import Blueprint,request,jsonify
from service.userService import create_user, login, getuser, updateUser


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
        if(result.get('error')):
            return jsonify(result),401
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
    

    
@userController.route('/update-user/<int:user_id>', methods=['PUT'])
def userupdate(user_id):
    try:
        data = request.get_json()
        result = updateUser(user_id, data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


