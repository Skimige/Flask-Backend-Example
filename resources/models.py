from resources import db
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION


class UserModel(db.Model):
    """
    UserModel

    table name: `users`

    - id: Integer (Primary Key)
    - username: String(40)
    - password: String(120)
    - email: String(40)
    - category: String(12)
    """
    __tablename__ = 'users'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    username = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    category = db.Column(db.String(12), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class BookModel(db.Model):
    """
    BookModel

    table name: `books`

    - id: Integer (Primary Key)
    - name: String(100)
    - description: String(100)
    - status: String(100)
    """
    __tablename__ = 'books'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Book {self.name}>'


class BookBorrowRecordModel(db.Model):
    """
    BookBorrowRecordModel

    table name: `books_borrow_history`

    - bookId: Integer (Primary Key)
    - userId: Integer
    - startAt: Double precision
    - endAt: Double precision
    """
    __tablename__ = 'books_borrow_history'

    bookId = db.Column(db.INTEGER, primary_key=True, nullable=False)
    userId = db.Column(db.INTEGER, nullable=False)
    startat = db.Column(type_=DOUBLE_PRECISION, nullable=False)
    endat = db.Column(type_=DOUBLE_PRECISION, nullable=False)

    def __repr__(self):
        return f'<BookBorrowRecord {self.bookId} @ {self.userId}>'
