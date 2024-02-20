from flask import Flask
from flask_bcrypt import Bcrypt
from config.dbconfig import init_app
from controller.userController import userController
from controller.audioController import audioController
from controller.testController import testController
from controller.dailySummaryController import dailySummaryController

app = Flask(__name__)
bcrypt = Bcrypt()
init_app(app)

app.register_blueprint(userController)
app.register_blueprint(audioController)
app.register_blueprint(testController)
app.register_blueprint(dailySummaryController)

if __name__ == '__main__':

    app.run(debug = True, host='localhost', port=9000)