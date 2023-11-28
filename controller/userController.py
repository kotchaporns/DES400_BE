from flask import Blueprint,request,jsonify
from service.userService import create_user, login

userController = Blueprint('userController', __name__)

@userController.route('/create-user', methods=['POST'])
def createUser():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'error':'username, email, and password are required'}), 400
        
        user = create_user(username, email, password)
        print(user)
        
        return jsonify({'success': 'Create user successfully', 'user_id': user.user_id, 'usernaem':user.username, 'email':user.email})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@userController.route('/login', methods=['GET'])
def userLogin():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error':'username, and password are required'}), 400
        
        result = login(email, password)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

