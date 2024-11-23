from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Book, Chapter, Page, UserBookInteraction

books = Namespace("books", description="A namespace for books")

book_model = books.model(
    "Book",
    {
        "book_id": fields.Integer(),
        "title": fields.String(),
        "author": fields.String(),
        "num_pages": fields.Integer(),
    }
)

chapter_model = books.model(
    "Chapter",
    {
        "chapter_id": fields.Integer(),
        "chapter_number": fields.Integer(),
        "start_page": fields.Integer(),
        "end_page": fields.Integer(),
        "content": fields.String()
    }
)

page_model = books.model(
    "Page",
    {
        "page_id": fields.Integer(),
        "page_number": fields.Integer(),
        "path_to_pdf": fields.String()
    }
)

interaction_model = books.model(
    "Interaction",
    {
        "score1": fields.Integer(),
        "score2": fields.Integer(),
        "score3": fields.Integer()
    }
)

@books.route("/books")
class BookListResource(Resource):
    @books.marshal_list_with(book_model)
    def get(self):
        """Returns all books"""
        books = Book.query.all()
        # Returns all books
        return books

    # add new book
    @jwt_required()
    @books.expect(book_model)
    def post(self):
        """Posts a book into the database"""
        data = request.get_json()

        new_title = data.get("title")
        new_author = data.get("author")
        new_length = data.get("num_pages")

        if not new_title or not new_author or not new_length:
            return jsonify({"Title, author, and length are required"}), 400

        new_book = Book(title=new_title, author=new_author, num_pages=new_length)
        new_book.save()

        return jsonify({f"Book '{new_title}' added successfully"}), 201

@books.route("/books/user")
class BookUserListResource(Resource):
    @books.marshal_list_with(book_model)
    @jwt_required
    def get(self):
        """Get all the books that the user has interacted with"""
        user_id = get_jwt_identity()
        userbooks = UserBookInteraction.query.filter_by(user_id=user_id).all()
        books = []
        for userbook in userbooks:
            book_id = userbook.book_id  # Assuming 'userbook' has a 'book_id' attribute
            book = Book.query.filter_by(book_id=book_id).first()  # Get the book by 'book_id'
            if book:
                books.append(book)
        return books

@books.route("/books/<int:book_id>/user")
class BookUserResource(Resource):
    @books.marshal_with(interaction_model)
    @jwt_required
    def get(self, book_id):
        user_id = get_jwt_identity()
        interaction = UserBookInteraction.query.filter_by(user_id=user_id, book_id=book_id).first_or_404()
        return interaction

    @books.expect(interaction_model)
    @jwt_required
    def post(self, book_id):
        """Create a user interaction with the book if it is a new interaction, updates the user interaction if it already exists"""
        user_id = get_jwt_identity

        data = request.get_json()

        score1 = data.get("score1")
        score2 = data.get("score2")
        score3 = data.get("score3")

        num_chapters = Chapter.query.filter_by(book_id=book_id).count()

        if UserBookInteraction.query.filter_by(book_id=book_id).first() is None:
            new_interaction = UserBookInteraction(book_id=book_id,
                                                  user_id=user_id,)
            new_interaction.save()

            return jsonify({"Interaction successfully created"}), 201
        else:
            toUpdate = UserBookInteraction.query.filter_by(book_id=book_id, user_id=user_id).first()
            toUpdate.update(score1, score2, score3)

            return jsonify({"Interaction successfully updated"}), 200


# book information
@books.route("/books/<int:book_id>")
class BookResource(Resource):

    @books.marshal_with(book_model)
    def get(self, book_id):
        """Returns book with specific book_id"""
        book = Book.query.get_or_404(book_id)
        return book

@books.route("books/<int:book_id>/chapters")
class ChapterListResource(Resource):

    @books.marshal_list_with(chapter_model)
    def get(self, book_id):
        """Returns all chapters given a book_id"""
        chapters = Chapter.query.filter_by(book_id=book_id).all()
        return chapters

    @books.expect(chapter_model)
    def post(self, book_id):
        """Post a chapter into the database given the book_id"""

        data = request.get_json()

        chapter_number = data.get("chapter_number")
        start_page = data.get("start_page")
        end_page = data.get("end_page")
        context = data.get("content")

        if not chapter_number or not start_page or not end_page or not context:
            return jsonify({"chapter_number, start_page, end_page, context are required"}), 400

        new_chapter = Chapter(book_id=book_id, chapter_number=chapter_number, start_page=start_page, end_page=end_page, context=context)
        new_chapter.save()

        return jsonify({"Chapter number: {chapter_number} for book id {book_id} has been created"}), 201


@books.route("chapters/<int:chapter_id>")
class ChapterResource(Resource):
    @books.marshal_with(chapter_model)
    def get(self, chapter_id):
        """Returns the chapter given a specific chapter_id"""

        chapter = Chapter.query.get_or_404(chapter_id)
        return chapter


@books.route("/books/<int:book_id>/chapters/<int:chapter_id>/pages")
class PageListResource(Resource):
    @books.marshal_list_with(page_model)
    def get(self, book_id, chapter_id):
        """Gets the pages of a specific chapter of a specific book"""

        pages = Page.query.filter_by(book_id=book_id, chapter_id=chapter_id).all()
        return pages

@books.route("chapters/<int:chapter_id>/pages")
class PagePostResource(Resource):
    @books.expect(page_model)
    def post(self, book_id, chapter_id):
        """Posts a page given the chapter and book id into the database"""

        data = request.get_json()

        page_number = data.get("page_number")
        path_to_pdf = data.get("path_to_pdf")

        new_page = Page(chapter_id=chapter_id, page_number=page_number, path_to_pdf=path_to_pdf)
        new_page.save()

        return jsonify({"Page number: {page_number} for chapter id: {chapter_id} has been successfully created"}), 201


@books.route("/pages/<int:page_id>")
class PageResource(Resource):
    @books.marshal_with(page_model)
    def get(self, page_id):
        """Returns a specific page given its id"""
        page = Page.query.get_or_404(page_id)
        return page


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


