import os
from dotenv import load_dotenv
from threading import Lock

def load_env():
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    if os.path.isfile(dotenv_path):
        load_dotenv(dotenv_path)


class Settings:
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                load_env()
                cls._instance = super(Settings, cls).__new__(cls)
                # Singleton para que los settings se inicialicen solo una vez
                cls._instance.mongo_db_url = os.environ.get('MONGO_DATABASE_URL')
                cls._instance.aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
                cls._instance.aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
                cls._instance.aws_email = os.environ.get('AWS_VERIFIED_EMAIL')
        return cls._instance


# Usage
settings = Settings()
