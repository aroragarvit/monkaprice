# we can import website folder and everything in init.py will run itself when we import website folder 


from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb.cursors
mysql=MySQL()                       # create your data base


def create_app():
    app=Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY']='GSsdgsdc'

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'ga_1142000'
    app.config['MYSQL_DB'] = 'users'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    mysql = MySQL(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")  # Register blueprint is a  python function

    return app

