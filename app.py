from flask import Flask
from flask_bcrypt import Bcrypt
from config.dbconfig import init_app
from controller.userController import userController
from controller.audioController import audioController
from controller.testController import testController

app = Flask(__name__)
bcrypt = Bcrypt()
init_app(app)

app.register_blueprint(userController)
app.register_blueprint(audioController)
app.register_blueprint(testController)

if __name__ == '__main__':

    app.run(debug = True, host='localhost', port=9000)