from flask import Blueprint, jsonify, request, abort, make_response
from app import db
# import datetime
from app.routes.routes_helper import *
from app.models.user import User

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

@user_bp.route('', methods=['POST'])
def add_user(): 
    request_body = request.get_json()
    user = validate_user(request_body)

    new_user = User.from_dict(user)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

# # get user_id and username upon login
@user_bp.route('/authenticate', methods=['POST'])
def login_user():
    request_body = request.get_json()
    user = validate_login(request_body['username'], request_body['password'])
    
    # returns user_id and username
    return jsonify(user.to_dict()), 200

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = validate_id(User, user_id)
    return jsonify(user.to_dict()), 200

#get all games associated with a user
@user_bp.route('/<user_id>/games', methods=['GET'])
def get_all_games_belonging_to_a_user(user_id):
    user = validate_id(User, user_id)
    
    games_response = [game.to_dict() for game in user.games]
    return jsonify({'games': games_response}), 200