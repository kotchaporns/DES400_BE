from flask import Blueprint,request,jsonify
from service.audioService import predictSnore

audioController = Blueprint('audioController', __name__)


@audioController.route('/send-audio', methods=['POST'])
def predict():
    try:
        file = request.files['audioFile']
        yhat, calls = predictSnore(file)
        return jsonify({'message':'Prediction Successful', 'Predict Result': {'yhat': str(yhat), 'calls': str(calls)}})


    except Exception as e:
      return jsonify({'error': str(e)}), 500