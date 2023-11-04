from dotenv import load_dotenv
import os

load_dotenv()
DB_URI = os.getenv('DB_URI')
DB_NAME = os.getenv('DB_NAME')
SECRET_KEY = os.getenv('SECRET_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'web_client/templates')
STATIC_DIR = os.path.join(ROOT_DIR, 'web_client/static')
