# SnoreWise_BE

## Installing Flask:

- pip install Flask
- pip install flask boto3
- pip install flask-sqlalchemy
- pip install Flask-Bcrypt
- pip install pymysql
- pip install -r requirements.txt


## run flask

- flask run 
- export FLASK_DEBUG=True / $env:FLASK_DEBUG = "True"



## create db.sqlite3

- flask shell
db.create_all()
exit()

- sqlite3 instance/db.sqlite3