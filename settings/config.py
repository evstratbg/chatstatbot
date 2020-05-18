import os
from pathlib import Path

import dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(Path(BASE_DIR, 'settings', 'env'))
IS_DEBUG = os.getenv('DEBUG') == '1'

BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_PORT = os.getenv('BOT_PORT', 8443)
BOT_IP = os.getenv('BOT_IP')
SSL_KEY = os.getenv('SSL_KEY')
SSL_CERT = os.getenv('SSL_CERT')
