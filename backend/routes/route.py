from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.model import Book, BookPage, ChapterPage
from models.model import User, Message
from models.model import Score
from db import db




books_ns = Namespace("books")

@books_ns.route("/books")
class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        result = [
            {
                "book_id": book.book_id,
                "book_name": book.book_name,
                "book_author": book.book_author,
                "book_page_num": book.book_page_num,
                "content": book.content,
            }
            for book in books
        ]
        return jsonify(result)


@books_ns.route("/bookpages")
class BookPageResource(Resource):
    def get(self):
        pages = BookPage.query.all()
        result = [
            {
                "book_id": page.book_id,
                "page_num": page.page_num,
                "page_text": page.page_text,
                "page_pdf": page.page_pdf,
            }
            for page in pages
        ]
        return jsonify(result)


@books_ns.route("/chapters")
class ChapterResource(Resource):
    def get(self):
        chapters = ChapterPage.query.all()
        result = [
            {
                "chapter_id": chapter.chapter_id,
                "book_id": chapter.book_id,
                "start_page": chapter.start_page,
                "end_page": chapter.end_page,
            }
            for chapter in chapters
        ]
        return jsonify(result)


scores_ns = Namespace("scores")

@scores_ns.route("/")
class ScoresResource(Resource):
    def get(self):
        scores = Score.query.all()
        result = [
            {
                "identification_score": score.identification_score,
                "catharsis_score": score.catharsis_score,
                "insight_score": score.insight_score,
                "score_total": score.score_total,
            }
            for score in scores
        ]
        return jsonify(result)
    

