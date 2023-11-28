from flask import Flask
from flask_bcrypt import Bcrypt
from config.dbconfig import init_app
from controller.userController import userController
from controller.audioController import audioController

app = Flask(__name__)
bcrypt = Bcrypt()
init_app(app)

app.register_blueprint(userController)
app.register_blueprint(audioController)

if __name__ == '__main__':

    app.run(debug = True)