# from flask import Flask
from resources import app, api
from resources.auth import Login, Register
from resources.routes.users import UsersAPI, UsersListAPI
from resources.routes.books import BooksAPI, BooksListAPI
from resources.routes.manage import BooksBorrowAPI, BooksReturnAPI


@app.route('/')
def hello_world():
    return 'Hello World!'


# Resource: Auth
api.add_resource(Register, '/register', endpoint='register')
api.add_resource(Login, '/login', endpoint='login')
# Resource: Users
api.add_resource(UsersListAPI, '/users', endpoint="users")
api.add_resource(UsersAPI, '/users/<string:id>', endpoint="user")
# Resource: Books
api.add_resource(BooksListAPI, '/books', endpoint="books")
api.add_resource(BooksAPI, '/books/<id>', endpoint="book")
# Resource: Borrow & Return
api.add_resource(BooksBorrowAPI, '/books/borrow/<id>', endpoint="borrow")
api.add_resource(BooksReturnAPI, '/books/return/<id>', endpoint="return")

if __name__ == '__main__':
    app.run()
