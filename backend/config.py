from decouple import config


class Config:
    SECRET_KEY = config("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATION = config('SQLALCHEMY_TRACK_MODIFICATION', cast=bool)


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URL = ""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    pass


class TestConfig(Config):
    pass
