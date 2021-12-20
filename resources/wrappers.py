from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_restful import abort
from resources import jwt
from resources.models import UserModel

blocklist = set()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blocklist


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        if UserModel.query.filter_by(username=identity).first().category == 'admin':
            return func(*args, **kwargs)
        else:
            abort(403, message='Not authorized.')
    return wrapper
