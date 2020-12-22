from hashlib import sha512

from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from api.models.user import UserModel

class User(Resource):
    def get(self, id):
        user = UserModel.find_by_id(id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404


class UserList(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}



_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help="This field cannot be blank."
                    )
_user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help="This field cannot be blank."
                    )

class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        data_password_hashed = sha512(data['password'].encode('utf-8')).hexdigest()
        if user and safe_str_cmp(data_password_hashed, user.password):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}
        return {'message': 'Invalid credentials'}, 401