from flask import Flask
from pymongo.mongo_client import MongoClient
from flask_login import LoginManager

# link to mongodb
db_uri = "mongodb+srv://ypeng24:CPSC1280@cluster0.aie0apy.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(db_uri)
db = client['tireder_db']
user_collection = db['users']


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'CPSC1280'
    app.config['MONGODB_SETTINGS'] = {
        'db': 'tireder_db',
        'host': db_uri
    }

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(uid):
        return user_collection.find_one({"id": uid})

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
