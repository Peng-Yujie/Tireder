from bson import ObjectId
from bson.errors import InvalidId
from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from config import DB_URI, DB_NAME, SECRET_KEY, TEMPLATE_DIR, STATIC_DIR
from flask_socketio import SocketIO

"""SOCKETIO"""
socketio = SocketIO()
"""MONGODB"""
client = MongoClient(DB_URI)
db = client[DB_NAME]
users = db["users_json"]
""""""


def create_app():
    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
    app.config['SECRET_KEY'] = SECRET_KEY
    socketio.init_app(app)

    from server.views import views
    from server.auth import auth
    from server.chatbot import chatbot

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(chatbot, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from server.models import User

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

    return app, socketio
