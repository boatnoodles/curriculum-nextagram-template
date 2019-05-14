from flask import Blueprint, jsonify
from models.user import User

users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"


@users_api_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.username == username)
    if not user:
        # Return the results in a json format, remember to be more verbose so the front end can parse the errors according
        resp = {'message': 'No user found with this username.',
                'status': 404}
        return jsonify(resp)

    resp = {'message': 'User found',
            'status': 200,
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'profileImg': user.profile_picture_url}
    return jsonify(resp)
