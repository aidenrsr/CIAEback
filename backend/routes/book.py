from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Book, Chapter, Page, UserBookInteraction
from ext import db


books = Namespace("books")

@books.route("/books")
class BookListResource(Resource):
    def get(self):  # all books
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

    # add new book
    @jwt_required()
    def post(self):
        data = request.get_json()
        title = data.get("title")
        author = data.get("author")
        length = data.get("length")

        if not title or not author or not length:
            return jsonify({"Title, author, and length are required"}), 400

        new_book = Book(title=title, author=author, length=length)
        new_book.save()

        return jsonify({f"Book '{title}' added successfully"}), 201
        
# book information
@books.route("/books/<int:book_id>")
class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        result = {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "length": book.length,
            "date_added": book.date_added,
            "chapters": [
                {
                    "chapter_id": chapter.chapter_id,
                    "title": chapter.title,
                    "chapter_number": chapter.chapter_number,
                    "start_page": chapter.start_page,
                    "end_page": chapter.end_page,
                }
                for chapter in book.get_chapters()
            ],
        }
        return jsonify(result)


@books.route("/pages")
class BookPageResource(Resource):
    def get(self):  # get all pages
        pages = Page.query.all()
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

    # add new page
    @jwt_required()
    def post(self):
        data = request.get_json()
        chapter_id = data.get("chapter_id")
        page_number = data.get("page_number")
        content = data.get("content")
        path = data.get("path")

        if not chapter_id or not page_number or not content or not path:
            return jsonify({"empty error"}), 400

        new_page = Page(chapter_id=chapter_id, page_number=page_number, content=content, path=path)
        new_page.save()
        return jsonify({"Page added successfully"}), 201

@books.route("/pages/<int:id>")
class PageResource(Resource):
    def get(self, page_id):
        page = Page.query.get_or_404(page_id)
        result = {
            "page_id": page.page_id,
            "chapter_id": page.chapter_id,
            "page_number": page.page_number,
            "content": page.content,
            "path": page.path,
        }
        return jsonify(result)

@books.route("/chapters")
class ChapterResource(Resource):
    def get(self):
        chapters = Chapter.query.all()
        result = [
            {
                "chapter_id": chapter.chapter_id,
                "book_id": chapter.book_id,
                "title" : chapter.title,
                "start_page": chapter.start_page,
                "end_page": chapter.end_page,
            }
            for chapter in chapters
        ]
        return jsonify(result)

    @jwt_required
    def post(self):
        data = request.get_json()
        book_id = data.get("book_id")
        title = data.get("title")
        chapter_number = data.get("chapter_number")
        start_page = data.get("start_page")
        end_page = data.get("end_page")

        if not book_id or not title or not chapter_number or not start_page or not end_page:
            return jsonify({"error": "All fields are required"}), 400

        new_chapter = Chapter(
            book_id=book_id, title=title, chapter_number=chapter_number, start_page=start_page, end_page=end_page
        )
        new_chapter.save()
        return jsonify({"chapter added successfully"}), 201


@books.route("/chapters/<int:chapter_id>")
class ChapterResource(Resource):
    def get(self, chapter_id):
        chapter = Chapter.query.get_or_404(chapter_id)
        result = [{
                    "page_id": page.page_id,
                    "page_number": page.page_number,
                    "content": page.content,
                    "path": page.path,
                }
                for page in chapter.get_pages()
        ]
        return jsonify(result)

    
@books.route("/books/<int:book_id>/interaction")
class BookInteractionResource(Resource):
    @jwt_required()
    def get(self, book_id):
        user_id = get_jwt_identity()
        interactions = UserBookInteraction.get_user_books(user_id)
        if not interactions:
            return jsonify({"No interaction found for this user"}), 404

        result = [{
            "user_id": interaction.user_id,
            "book_id": interaction.book_id,
            "progress": interaction.progress,
            "score1": interaction.score1,
            "score2": interaction.score2,
            "score3": interaction.score3,
            } 
            for interaction in interactions 
        ]
        return jsonify(result)

    @jwt_required()
    def post(self, book_id):
        user_id = get_jwt_identity()
        data = request.get_json()
        # current progress
        progress = data.get("progress")
        score1 = data.get("score1")
        score2 = data.get("score2")
        score3 = data.get("score3")
        # 
        interaction = UserBookInteraction.query.filter_by(user_id=user_id, book_id=book_id).first()

        if interaction:
            interaction.progress = progress
            interaction.score1 = score1
            interaction.score2 = score2
            interaction.score3 = score3
        else:
            interaction = UserBookInteraction(
                user_id=user_id, book_id=book_id, progress=progress, score1=score1, score2=score2, score3=score3
            )
        interaction.save()

        return jsonify({"Interaction updated successfully"}), 200


