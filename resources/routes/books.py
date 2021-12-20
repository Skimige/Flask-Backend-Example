from resources import db
from resources.wrappers import admin_required
from resources.models import BookModel
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt_identity


########################################
# route: /books
########################################

# GET: 获取书本列表
# POST: 创建新书本
class BooksListAPI(Resource):
    """
    书本列表

    - GET: 获取书本列表
    - POST: 创建新书本
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        books = BookModel.query.all()
        result = [
            {
                'id': book.id,
                'name': book.name,
                'description': book.description,
                'status': book.status
            } for book in books
        ]
        return result

    @admin_required
    def post(self):
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('description', type=str)
        self.parser.add_argument('status', type=str)

        args = self.parser.parse_args()
        name = args['name']
        description = args['description']
        status = args['status']

        book = BookModel(
            id=BookModel.query.order_by(BookModel.id.desc()).first().id + 1,
            name=name,
            description=description,
            status=status
        )

        db.session.add(book)
        db.session.commit()

        return {
            'success': 0,
            'id': book.id,
            'name': book.name
        }


class BooksAPI(Resource):
    """
    书本

    - GET: 获取某书本信息
    - PUT: 编辑书本信息
    - DELETE: 删除书本
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @jwt_required
    def get(self, id):
        try:
            book = BookModel.query.get(int(id))
        except ValueError:
            abort(400, message='Illegal book id given!')
        result = {
            'id': book.id,
            'name': book.name,
            'description': book.description,
            'status': book.status
        }
        return result

    @admin_required
    def put(self, id):
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('description', type=str)
        self.parser.add_argument('status', type=str)

        args = self.parser.parse_args()
        name = args['name']
        description = args['description']
        status = args['status']

        target = BookModel.query.get(int(id))
        target.name = name if name is not None else target.name
        target.description = description if description is not None else target.description
        target.status = status if status is not None else target.status

        db.session.commit()
        target = BookModel.query.get(int(id))
        return {
            'success': 0,
            'id': target.id,
            'name': target.name,
            'description': target.description,
            'status': target.status
        }

    @admin_required
    def delete(self, id):
        target = BookModel.query.get(int(id))
        db.session.delete(target)
        db.session.commit()
        return {
            'success': 0,
            'id': id
        }
