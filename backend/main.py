from flask import Flask
from flask_restx import Api, Resource, fields
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
from ext import db
from models import User, Book, Chapter, Page, UserBookInteraction, UserPoint, UserPerformance, Page

from auth import auth_ns
from routes.ai import ai_ns
from routes.book import book_ns
from routes.community import community
from routes.user import user


app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

api = Api(app, doc='/docs')

JWTManager(app)
api.add_namespace(auth_ns)
api.add_namespace(ai_ns)
api.add_namespace(book_ns)
api.add_namespace(community)
api.add_namespace(user)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.errorhandler(404)
def not_found(err):
    return app.send_static_file("index.html")


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Book": Book,
        "Chapter": Chapter,
        "Page": Page,
        "UserBookInteraction": UserBookInteraction,
        "UserPoint": UserPoint,
        "UserPerformance": UserPerformance
    }


if __name__ == "__main__":
    app.run(debug=True)
