import os

PROFILE = False

PROFILE_CONFIG = {
    "enabled": PROFILE,
    "basicAuth": {"enabled": True, "username": "admin", "password": "admin"},
    "ignore": ["^/static/.*"],
}

USERNAME = os.getenv("DB_USER", "an_user")
PASSWORD = os.getenv("DB_PASSWORD", "a_password")
DB = os.getenv("DB_NAME", "neuralworks")
HOST = os.getenv("DB_HOST", "localhost")

SQLALCHEMY_DATABASE_URI = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:5432/{DB}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
