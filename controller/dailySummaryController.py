from flask import Blueprint,request,jsonify, send_file
from service.dailySummaryService import getDaily, updateDailyFactor, getSound, cal_notification, getPdf
from flask.helpers import make_response
import os




dailySummaryController = Blueprint('dailySummaryController', __name__)


@dailySummaryController.route('/get-daily', methods=['GET'])
def userGetDaily():
    try:
        user_id = request.args.get('user_id')
        date = request.args.get('date')

        daily = getDaily(user_id, date)
        
        return jsonify({'message':'success', 'response':daily})
    except Exception as e:
      return jsonify({'error': str(e)}), 500
    

@dailySummaryController.route('/update-factor', methods=['PUT'])
def userGeuserUpdatetDailyFactor():
    try:
        data = request.get_json()
        result = updateDailyFactor(data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@dailySummaryController.route('/notify/<int:user_id>', methods=['POST'])
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
    



    

@dailySummaryController.route('/request-sound', methods=['GET'])
def getrequestsound():
    try:
        user_id = request.args.get('user_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        records = getSound(user_id, start_date, end_date)
        
        return jsonify({'message':'success', 'response':records})
    except Exception as e:
      return jsonify({'error': str(e)}), 500
    



    
@dailySummaryController.route('/pdf', methods=['GET'])
def requestPdf():
    try:
        user_id = request.args.get('user_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        filename = 'snorewise_rpt.pdf'


        pdf_file = getPdf(user_id, start_date, end_date)
        
        return send_file(pdf_file, as_attachment=True, download_name=filename)
        # return jsonify({'message':'success'})
        # if isinstance(pdf_file, dict):
        #     # Handle the error case
        #     print(pdf_file['error'])
        # else:
        #     # Send the buffer as a response (e.g., in a Flask route)
        #     response = make_response(pdf_file.getvalue())
        #     response.headers['Content-Type'] = 'application/pdf'
        #     response.headers['Content-Disposition'] = f'inline; filename={filename}'

    except Exception as e:
      return jsonify({'error': str(e)}), 500

    