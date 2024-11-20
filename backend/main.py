from flask import Flask
from flask_restx import Api, Resource, fields
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
from ext import db


app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

api = Api(app, doc='/docs')

JWTManager(app)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db
    }


if __name__ == "__main__":
    app.run(debug=True)
