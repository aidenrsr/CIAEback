from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")  # Fallback if SECRET_KEY isn't provided
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() in ["true", "1"]


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEV_DATABASE_URL", "postgresql+psycopg2://postgres:postgres@/flaskdb?host=/cloudsql/ciae-442621:asia-northeast3:ciae-back-dev"
    )
    DEBUG = True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "PROD_DATABASE_URL", "postgresql://production:1234@localhost:5432/production"
    )
    DEBUG = False
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() in ["true", "1"]


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URL", "postgresql://testing:1234@localhost:5432/testing"
    )
    TESTING = True

