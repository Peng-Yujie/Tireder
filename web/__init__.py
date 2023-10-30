from bson import ObjectId
from bson.errors import InvalidId
from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Connect to mongodb
load_dotenv()
DB_URI = os.getenv('DB_URI')  # Replace with your connection string
DB_NAME = os.getenv('DB_NAME')  # Replace with your DB name
client = MongoClient(DB_URI)
db = client[DB_NAME]
users = db["users_json"]  # Replace with your collection name


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Replace with your secret key

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from services.models import User

    @login_manager.user_loader
    def load_user(uid):
        try:
            user_json = users.find_one({"_id": ObjectId(uid)})
            if user_json:
                return User(user_json)
            else:
                return None
        except InvalidId:
            return None

    return app
