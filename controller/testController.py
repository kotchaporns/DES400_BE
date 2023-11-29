from flask import Blueprint,request,jsonify


testController = Blueprint('testController', __name__)

@testController.route('/', methods=['GET'])
def hello():
    return "Hello, snorewise!"