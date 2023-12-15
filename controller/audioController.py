from flask import Blueprint,request,jsonify
from service.audioService import predictSnore, getDaily, updateDailyFactor, cal_notification

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
    
@audioController.route('/get-daily', methods=['GET'])
def userGetDaily():
    try:
        user_id = request.args.get('user_id')
        date = request.args.get('date')

        daily = getDaily(user_id, date)
        
        return jsonify({'message':'success', 'response':daily})
    except Exception as e:
      return jsonify({'error': str(e)}), 500
    

@audioController.route('/update-factor', methods=['PUT'])
def userGeuserUpdatetDailyFactor():
    try:
        data = request.get_json()
        result = updateDailyFactor(data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@audioController.route('/notify/<int:user_id>', methods=['POST'])
def get_notification(user_id):

    try:
        notification_data = cal_notification(user_id)

        if notification_data is not None:
            return jsonify(notification_data), 200 # Return as JSON response
        else:
            # Return an error response if cal_notification returns None
            return jsonify({'error': 'An error occurred while processing the request.'}), 500

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


