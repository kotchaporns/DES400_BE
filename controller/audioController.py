from flask import Blueprint,request,jsonify
from service.audioService import predictSnore

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
        record, calls = predictSnore(file, user_id, date, time_start, time_stop)
        return jsonify({'message':'Prediction Successful', 'response': {'model_result': record.model_result, 'calls': str(calls), 'user_id':user_id, 'date': date, 'time_start':time_start, 'time_stop':time_stop}})
        # return jsonify({'message': 'success'})
    

    except Exception as e:
      return jsonify({'error': str(e)}), 500