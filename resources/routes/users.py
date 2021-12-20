from resources import db
from resources.wrappers import admin_required
from resources.models import UserModel
from resources.utils import pwd_encrypt
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt_identity


########################################
# route: /users
########################################

class UsersListAPI(Resource):
    """
    用户列表

    - GET: 获取用户列表
    - POST: 创建新用户（需 `admin` 权限）
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @admin_required
    def get(self):
        users = UserModel.query.all()
        result = [
            {
                "id": user.id,
                "username": user.username,
                # "password": user.password,
                "email": user.email,
                "category": user.category
            } for user in users
        ]
        return result

    @admin_required
    def post(self):
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('category', type=str)
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        email = args['email']
        category = args['category']
        user = UserModel(
            id=UserModel.query.order_by(UserModel.id.desc()).first().id + 1,
            username=username, password=pwd_encrypt(password),
            email=email,
            category=category)
        db.session.add(user)
        db.session.commit()
        return {
            'success': 0,
            'username': username
        }


class UsersAPI(Resource):
    """
    用户

    - GET: 获取某用户信息（非 `self` 需 `admin` 权限）；self - 获取自己的信息
    - PUT: 修改用户信息（需 `admin` 权限）
    - DELETE: 删除用户（需 `admin` 权限）
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @jwt_required
    def get(self, id):
        if id == 'self':
            identity = get_jwt_identity()
            user = UserModel.query.filter_by(username=identity).first()
            result = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "category": user.category
            }
        else:
            try:
                user = UserModel.query.get(int(id))
            except ValueError:
                abort(400, message='Illegal user id given!')
            result = {
                    "id": user.id,
                    "username": user.username
            }
            user_identity = get_jwt_identity()
            if UserModel.query.filter_by(username=user_identity).first().category == 'admin':
                result['email'] = user.email
                result['category'] = user.category
        return result

    @admin_required
    def put(self, id):
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('category', type=str)

        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        email = args['email']
        category = args['category']

        target = UserModel.query.get(int(id))
        target.username = username if username is not None else target.username
        target.password = pwd_encrypt(password) if password is not None else target.password
        target.email = email if email is not None else target.email
        target.category = category if category is not None and target.category != 'admin' else target.category

        db.session.commit()
        target = UserModel.query.get(int(id))
        return {
            'success': 0,
            'id': target.id,
            'username': target.username,
            'email': target.email,
            'category': target.category,
            'password_changed': True if password else False
        }

    @admin_required
    def delete(self, id):
        target = UserModel.query.get(int(id))
        db.session.delete(target)
        db.session.commit()
        return {
            'success': 0,
            'id': id
        }
