from backend.ext import db


class User(db.Model):
    """
    User Model:
    - id: Integer (Primary Key)
    - username: String (Unique)
    - email: String
    - password: String
    - points: Integer
    - created_at: Date
    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    points = db.Column(db.Integer(), nullable=False, default=0)
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())

    def __repr__(self):
        return f"<User {self.username}>"

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

    __tablename__ = "userperformances"

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


class Book(db.Model):
    """
    Book Model:
    - book_id: Integer (Primary Key)
    - title: String
    - author: String
    - num_pages: Integer
    """

    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    num_pages = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"

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
    - chapter_number: Integer
    - start_page: Integer
    - end_page: Integer
    - content: text
    """

    __tablename__ = "chapters"

    chapter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    chapter_number = db.Column(db.Integer, nullable=False)
    start_page = db.Column(db.Integer, nullable=False)
    end_page = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Chapter {self.chapter_number} of Book {self.book_id}>"

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
    - path_to_pdf: String
    """

    __tablename__ = "pages"

    page_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.chapter_id"), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    path_to_pdf = db.Column(db.String(80), nullable=False)

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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    progress = db.Column(db.Float, nullable=False, default=0.0)
    score1 = db.Column(db.Integer, nullable=False, default=0)
    score2 = db.Column(db.Integer, nullable=False, default=0)
    score3 = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<BookUserInteraction User {self.user_id} - Book {self.book_id}: {self.progress}%>"

    def update(self, newScore1, newScore2, newScore3):
        num_chapter = Chapter.query.filter_by(book_id=self.book_id).count()
        self.score1 = (self.progress*num_chapter*self.score1+newScore1)/(self.progress*num_chapter+1)
        self.score2 = (self.progress*num_chapter*self.score2+newScore2)/(self.progress*num_chapter+1)
        self.score3 = (self.progress*num_chapter*self.score3+newScore3)/(self.progress*num_chapter+1)
        self.progress += 1/num_chapter

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Thread(db.Model):
    """
    Thread Model
    """
    __tablename__ = "threads"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=True)  # Optional link to a book


    def __repr__(self):
        return f"<Thread {self.title}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Post(db.Model):
    """
    Post Model
    """
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thread_id = db.Column(db.Integer, db.ForeignKey("threads.id"), nullable=False)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Post {self.title}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Comment(db.Model):
    """
    Comment Model:
    """

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    username = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


    def __repr__(self):
        return f"<Comment {self.content}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class GameScore(db.Model):

    __tablename__ = "gamescore"

    score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<GameScore User {self.user_id}, Score {self.score}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
