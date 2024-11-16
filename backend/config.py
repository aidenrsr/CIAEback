from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY')
