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

# Namespace
messages_ns = Namespace("messages")
message_model = messages_ns.model(
    "Message",
    {
        "message_id": fields.Integer(),
        "username": fields.String(),
        "text": fields.String(),
        "timestamp": fields.DateTime(),
    },
)


@messages_ns.route("/messages")
class MessagesResource(Resource):
    @messages_ns.marshal_list_with(message_model)
    def get(self):
        chat = Message.query.order_by(Message.timestamp.asc()).all()
        return chat

    @messages_ns.expect(message_model)
    @messages_ns.marshal_with(message_model)
    @jwt_required()
    def post(self):
        # get the user id from JWT
        user_id = get_jwt_identity()
        # fetch the user from the database
        user = User.query.get_or_404(user_id)
        # get the message text from the request body
        data = request.get_json()
        text = data.get('text', '').strip()
        if not text:
            return {'Message cannot be empty'}, 400
        # create and save the message
        message = Message(username = user.username, text = text)
        db.session.add(message)
        db.session.commit()

        return {'Message sent'}, 201

@messages_ns.route("/messages/<int:message_id>")
class MessageResource(Resource):
    @messages_ns.marshal_with(message_model)
    def get(self, message_id):
        message = Message.query.get_or_404(message_id)
        return message

    @jwt_required()
    def delete(self, message_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        message_to_delete = Message.query.get_or_404(message_id)
        # check if user and message writer match
        if user.username != message_to_delete.username:
            return {"error"}, 403
        
        db.session.delete(message_to_delete)
        db.session.commit()
        return {"Message deleted"}, 200
    

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
    

