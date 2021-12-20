from resources import db
from resources.models import UserModel, BookModel, BookBorrowRecordModel
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
import time


class BooksBorrowAPI(Resource):
    """
    书本借出
    - GET: 查询可用性
    - POST: 借书
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @jwt_required
    def get(self, id):
        target = BookBorrowRecordModel.query.filter_by(bookId=id).order_by(BookBorrowRecordModel.startat.desc()).first()
        if target is not None:
            availability = False
            if time.time() > target.endat:
                message = 'This book has been borrowed, and has expired its returning time. ' \
                          'Sorry for any inconvenience,'
            else:
                message = 'This book has been borrowed, and is still in reading period. Please wait for its returning.'
        else:
            availability = True
            message = 'This book is available now.'
        return {
            'bookId': id,
            'available': availability,
            'message': message
        }

    @jwt_required
    def post(self, id):
        target = BookBorrowRecordModel.query.filter_by(bookId=id).order_by(BookBorrowRecordModel.startat.desc()).first()
        target_book = BookModel.query.filter_by(id=id).first()
        print(target_book)
        if target is not None:
            return {
                'success': 1,
                'message': 'This book is not available'
            }, 403
        else:
            borrow_time = time.time()
            return_time = borrow_time + 1209600
            new_borrow = BookBorrowRecordModel(
                bookId=id,
                userId=UserModel.query.filter_by(username=get_jwt_identity()).first().id,
                startat=borrow_time,
                endat=return_time
            )
            target_book.status = 'unavailable'
            db.session.add(new_borrow)
            db.session.commit()
            return {
                'success': 0,
                'bookId': new_borrow.bookId,
                'startat': new_borrow.startat,
                'endat': new_borrow.endat
            }


class BooksReturnAPI(Resource):
    """
    书本归还
    - POST: 还书
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @jwt_required
    def post(self, id):
        userid = UserModel.query.filter_by(username=get_jwt_identity()).first().id
        target = BookBorrowRecordModel.query.filter_by(bookId=id).filter_by(userId=userid).first()
        target_book = BookModel.query.filter_by(id=id).first()
        if target is not None:
            return_time_actual = time.time()
            if return_time_actual > target.endat:
                message = 'Returned book exceeding reading period.'
            else:
                message = 'Returned book in time.'
            target_book.status = 'available'
            db.session.delete(target)
            db.session.commit()
            return {
                'success': 0,
                'bookId': target.bookId,
                'endat': target.endat,
                'actual_endat': return_time_actual,
                'message': message
            }
