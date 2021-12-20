from flask import jsonify
from flask_restful import Resource, reqparse, abort
from resources import db, jwt
from resources.routes.users import UserModel
from resources.utils import pwd_encrypt, pwd_verify
from flask_jwt_extended import create_access_token


########################################
# route: authenticate
########################################


# /login: GET
class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        self.parser.add_argument('username', type=str, required=True, help='Username is empty')
        self.parser.add_argument('password', type=str, required=True, help='Password is empty')

        args = self.parser.parse_args()
        username = args['username']
        password = args['password']

        user = UserModel.query.filter_by(username=username).first()
        if pwd_verify(password, user.password):
            ak = create_access_token(identity=username, fresh=True)
            return jsonify(access_token=ak)


# /register: POST
class Register(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument('username', type=str, required=True, help='Username is empty')
        self.parser.add_argument('password', type=str, required=True, help='Password is empty')
        self.parser.add_argument('email', type=str, required=True, help='Email is empty')

        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        email = args['email']

        if UserModel.query.filter_by(username=username).first() is not None:
            abort(400, message=f'User {username} already exists.')
        if UserModel.query.filter_by(email=email).first() is not None:
            abort(400, message=f'Email {username} already exists.')

        user = UserModel(
            id=UserModel.query.order_by(UserModel.id.desc()).first().id + 1,
            username=username, password=pwd_encrypt(password),
            email=email,
            category='user'
            )
        db.session.add(user)
        db.session.commit()
        ak = create_access_token(username, fresh=True)

        return {
            'success': 0,
            'username': username,
            'access_token': ak
        }
