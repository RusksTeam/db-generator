from flask_restful import Resource, reqparse
from api.models.drybread import DryBreadModel
from flask_jwt_extended import jwt_required, get_jwt_claims

class DryBread(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('question',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')
    parser.add_argument('answer',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    @jwt_required
    def get(self, _id):
        drybread = DryBreadModel.find_by_id(_id)
        if drybread:
            return drybread.json()
        return {'message': 'Drybread not found.'}, 404


    #POST method doesn't need and _id argument. Waiting for response from udemy on how it should be implemented properly
    @jwt_required
    def post(self, _id=None):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin rights required.'}
        data = DryBread.parser.parse_args()
        drybread = DryBreadModel(**data)
        try:
            drybread.save_to_db()
        except:
            return {'message': 'Error occured when saving drybread to database.'}, 500

        return drybread.json(), 201


    @jwt_required
    def delete(self, _id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin rights required.'}
        drybread = DryBreadModel.find_by_id(_id)
        if drybread:
            try:
                drybread.delete_from_db()
            except:
                return {'message', 'Error occured when removing drybread from database.'}, 500
            return {'message': 'Drybread deleted.'}
        return {'message': 'Drybread not found.'}


    @jwt_required
    def put(self, _id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin rights required.'}
        data = DryBread.parser.parse_args()
        drybread = DryBreadModel.find_by_id(_id)
        if drybread:
            drybread.question = data['question']
            drybread.answer = data['answer']
        else:
            drybread = DryBreadModel(**data)
        try:
            drybread.save_to_db()
        except:
            return {'message', 'Error occured when updating drybread.'}, 500

        return drybread.json()


class DryBreadList(Resource):

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin rights required.'}
        return {'drybreads': [x.json() for x in DryBreadModel.find_all()]}