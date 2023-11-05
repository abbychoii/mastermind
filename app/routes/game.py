from flask import Blueprint, jsonify, request, abort, make_response
from app import db
# import datetime
from app.routes.routes_helper import *
from app.models.game import Game
from app.models.guess import Guess

game_bp = Blueprint('game_bp', __name__, url_prefix='/game')

@game_bp.route('', methods=['POST']) 
def create_game():
    request_body = request.get_json()
    validated_game = validate_game_request(request_body)
    new_game_dict = generate_number_combo(validated_game)
    if 'user_id' in request_body: 
        user = validate_id(User, request_body['user_id'])
        new_game_dict['user_id'] = user.user_id

    new_game = Game.from_dict(new_game_dict)
    db.session.add(new_game)
    db.session.commit()
    return jsonify(new_game.to_dict()), 201

@game_bp.route('/<game_id>/guess', methods=['POST'])
def create_guess(game_id):
    game = validate_id(Game, game_id)
    request_body = request.get_json()
    game_info = validate_guess(request_body['guess'], game)

    guess_dict = calculate_guess_feedback(game_info)
    new_guess = Guess.from_dict({'guess': request_body['guess'], 'game_id': game_id, 'corr_num': guess_dict['corr_num'], 'corr_loc': guess_dict['corr_loc'], 'feedback': guess_dict['feedback']})

    if guess_dict['game_won']:
        game.game_won = guess_dict['game_won']
    
    db.session.add(new_guess)
    db.session.commit()
    return jsonify(new_guess.to_dict()), 201

@game_bp.route('/<game_id>', methods=['GET'])
def get_game(game_id):
    game = validate_id(Game, game_id)
    return jsonify(game.to_dict()), 200

@game_bp.route('/<game_id>/guess', methods=['GET'])
def get_guesses(game_id):
    game = validate_id(Game, game_id)
    return jsonify({'guesses' : game.guesses_for_game()}), 200

@game_bp.route('/<game_id>/hint', methods=['GET'])
def get_hint(game_id):
    game = validate_id(Game, game_id)
    hint = generate_hint(game)
    return jsonify(hint), 200
    