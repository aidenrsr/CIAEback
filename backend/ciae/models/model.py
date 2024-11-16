from db import db
from datetime import datetime, timezone

'''
user
'''

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text)
    oauth_provider = db.Column(db.Text)
    oauth_user_id = db.Column(db.Text, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

'''
message
'''

class Message(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

'''
book related model for db
'''

class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.Text, nullable=False)
    book_author = db.Column(db.Text, nullable=False)
    book_page_num = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

class BookPage(db.Model):
    __tablename__ = 'book_page'
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    page_num = db.Column(db.Integer, primary_key=True)
    page_text = db.Column(db.Text, nullable=False)
    page_pdf = db.Column(db.Text, nullable=False)


class ChapterPage(db.Model):
    __tablename__ = 'chapter_page'
    chapter_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    start_page = db.Column(db.Integer, nullable=False)
    end_page = db.Column(db.Integer, nullable=False)

'''
scores
'''

class Score(db.Model):
    __tablename__ = 'score'

    identification_score = db.Column(db.Integer, nullable=False)
    catharsis_score = db.Column(db.Integer, nullable=False)
    insight_score = db.Column(db.Integer, nullable=False)
    score_total = db.Column(db.Integer, nullable=False)
