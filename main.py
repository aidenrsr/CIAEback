from flask import Flask
from flask_restx import Api, Resource, fields
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from backend.config import DevConfig
from backend.ext import db
from backend.models import User, Book, Chapter, Page, UserBookInteraction, UserPerformance, Page, GameScore

from backend.auth import auth_ns
from backend.routes.ai import ai_ns
from backend.routes.book import books
from backend.routes.user import user_ns
from backend.routes.community import community_ns
from backend.routes.score import game_score_ns


app = Flask(__name__)
app.config.from_object(DevConfig)
CORS(app)

db.init_app(app)

api = Api(app, doc='/docs')

JWTManager(app)
api.add_namespace(auth_ns)
api.add_namespace(ai_ns)
api.add_namespace(books)
api.add_namespace(community_ns)
api.add_namespace(user_ns)
api.add_namespace(game_score_ns)


@app.shell_context_processor
def make_shell_context():
    return {
        "User": User,
        "db": db,
        "Book": Book,
        "Chapter": Chapter,
        "Page": Page,
        "UserBookInteraction": UserBookInteraction,
        "UserPerformance": UserPerformance,
        "GameScore": GameScore
    }


if __name__ == "__main__":
    app.run(port=8080, debug=True, host='0.0.0.0')
