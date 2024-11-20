from main import db


class User(db.Model):
    """
    User Model:
    - id: Integer (Primary Key)
    - username: String (Unique)
    - email: String
    - password: String
    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())

    points = db.relationship("UserPoint", back_populates="user", cascade="all, delete-orphan")
    performance = db.relationship("UserPerformance", back_populates="user", cascade="all, delete-orphan")
    book_interactions = db.relationship("UserBookInteraction", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

    def get_points(self):
        """ return points the user has """
        return self.points

    def get_performance(self):
        """ retuns user performance score """
        return self.performance

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserPerformance(db.Model):
    """
    UserPerformacne Model:
    - user_id: Integer (Foreign Key)
    - score1: Integer
    - score2: Integer
    - score3: Integer
    """

    __tablenane__ = "userperformances"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    score1 = db.Column(db.Integer, nullable=False)
    score2 = db.Column(db.Integer, nullable=False)
    score3 = db.Column(db.Integer, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserPoint(db.Model):
    """
    UserPoint Model:
    - user_id: Integer (Foreign Key)
    - points: Integer
    """

    __tablename__ = "userpoints"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    points = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<UserPoint User {self.user_id} Points {self.points}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Book(db.Model):
    """
    Book Model:
    - book_id: Integer (Primary Key)
    - title: String
    - author: String
    - date_added: Date
    """

    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    date_added = db.Column(db.Date(), default=db.func.current_date())

    # Relationship with chapters
    chapters = db.relationship("Chapter", back_populates="book", cascade="all, delete-orphan")
    user_interactions = db.relationship("UserBookInteraction", back_populates="book")

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"

    def get_chapters(self):
        """ returns all chapters of the book """
        return self.chapters

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Chapter(db.Model):
    """
    Chapter Model:
    - chapter_id: Integer (Primary Key)
    - book_id: Integer (Foreign Key)
    - title: String
    - chapter_number: Integer
    """

    __tablename__ = "chapters"

    chapter_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    title = db.Column(db.String(), nullable=False)
    chapter_number = db.Column(db.Integer, nullable=False)

    # Relationship with book
    book = db.relationship("Book", back_populates="chapters")

    # Relationship with pages
    pages = db.relationship("Page", back_populates="chapter", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Chapter {self.chapter_number}: {self.title} of Book {self.book_id}>"

    def getpages(self):
        """ returns all pages of the chapter """
        return self.pages

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Page(db.Model):
    """
    Page Model:
    - page_id: Integer (Primary Key)
    - chapter_id: Integer (Foreign Key)
    - page_number: Integer
    - content: String
    """

    __tablename__ = "pages"

    page_id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.chapter_id"), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Relationship with chapter
    chapter = db.relationship("Chapter", back_populates="pages")

    def __repr__(self):
        return f"<Page {self.page_number} of Chapter {self.chapter_id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserBookInteraction(db.Model):
    """
    Class UserBookInteraction:
        id:Integer (Primary Key)
        book_id:Integer (Foreign Key)
        user_id:Integer (Foregin Key)
        progress:Float
        score1:Integer
        score2:Integer
        score3:Integer
    """

    __tablename__ = "userbookinteractions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    progress = db.Column(db.Float, nullable=False, default=0.0)
    last_interaction = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    score1 = db.Column(db.Integer, nullable=False)
    score2 = db.Column(db.Integer, nullable=False)
    score3 = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", back_populates="book_interactions")
    book = db.relationship("Book", back_populates="user_interactions")

    def __repr__(self):
        return f"<BookUserInteraction User {self.user_id} - Book {self.book_id}: {self.progress}%>"

    @classmethod
    def get_user_books(cls, user_id):
        """
        Get all books a user has read or is reading, along with progress.
        :param user_id: User ID
        :return: List of books with progress
        """
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_book_info(cls, user_id, book_id):
        """
        Get the info of a user in a specific book.
        :param user_id: User ID
        :param book_id: Book ID
        :return: Progress in percentage
        """
        interaction = cls.query.filter_by(user_id=user_id, book_id=book_id).first()
        return interaction.progress if interaction else None

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Tread(db.Model):
    """
    class Tread:
     - id:Integer (Primary Key)
     - title:String
     - book_id:Integer (Foreign Key)
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=True)  # Optional

    def __repr__(self):
        return f"Thread {self.title}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Post(db.Model):
    """
    class Post:
     - id:Integer (Primary Key)
     - thread_id:Integer (Foreign Key)
     - creator_id:Integer (Foregin Key)
     - title:String
     - content:Text
     - create_time:datetime
    """


class Comment(db.Model):
    """
    class Comment:
     - id:Integer (Primary Key)
     - post_id:Integer (Foreign Key)
     - creator_id:Integer (Foregin Key)
     - title:String
     - content:Text
     - create_time:datetime
    """


