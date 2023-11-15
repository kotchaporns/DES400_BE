from flask import Flask
from audioApi import audio_api

app = Flask(__name__)
app.register_blueprint(audio_api)

@app.route('/hello-world')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run()