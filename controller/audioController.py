from flask import Blueprint,request,jsonify
from service.audioService import predictSnore, getpredict

audioController = Blueprint('audioController', __name__)


@audioController.route('/send-audio', methods=['POST'])
def predict():
    try:
        file = request.files['audioFile']
        user_id = request.form['user_id']
        date = request.form['date']
        time_start = request.form['time_start']
        time_stop = request.form['time_stop']
        # print(user_id)
        record = predictSnore(file, user_id, date, time_start, time_stop)
        return jsonify({'message':'Prediction Successful', 'response': {'model_result': record.model_result, 'calls': record.calls, 'user_id':user_id, 'date': date, 'time_start':time_start, 'time_stop':time_stop, 'S3_path': record.path}})
        # return jsonify({'message': 'success'})
    

    except Exception as e:
      return jsonify({'error': str(e)}), 500
    
    
@audioController.route('/getpredict', methods=['POST'])
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
    
