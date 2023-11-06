from flask import abort, make_response
from app.models.user import User
from app.models.game import Game    
from app.models.guess import Guess

import requests, collections

#Helper functions that will be used in multiple routes
# validate id, validate login, generate number combo, validate guess, calculate guess feedback

def validate_id(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{cls.__name__} {id} invalid. ID must be an integer."},400))
    
    item = cls.query.get(id)

    if not item:
        abort(make_response({"message":f"{cls.__name__} {id} not found"}, 404))
    
    return item

def validate_game_request(request):
    # Define default values
    default_num_min = 0
    default_num_max = 7
    default_code_length = 4
    default_guesses_allowed = 10

    if 'num_min' in request:
        try:
            num_min = int(request['num_min'])
            if num_min < 0:
                raise ValueError
        except ValueError:
            abort(make_response({'message': 'num_min must be a non-negative integer.'}, 400))
    else:
        num_min = default_num_min

    if 'num_max' in request:
        try:
            num_max = int(request['num_max'])
            if num_max >= 9 or num_min >= num_max:
                raise ValueError
        except ValueError:
            abort(make_response({'message': 'num_max must be an integer less than 9 and greater than num_min.'}, 400))
    else:
        num_max = default_num_max

    if 'code_length' in request:
        try:
            code_length = int(request['code_length'])
            if code_length <= 1 or code_length > 10:
                raise ValueError
        except ValueError:
            abort(make_response({'message': 'code_length must be an integer between 2 and 10, inclusive.'}, 400))
    else:
        code_length = default_code_length

    if 'guesses_allowed' in request:
        try:
            guesses_allowed = int(request['guesses_allowed'])
            if guesses_allowed >= 20 or guesses_allowed < 2:
                raise ValueError
        except ValueError:
            abort(make_response({'message': 'guesses_allowed must be an integer between 2 and 20, inclusive.'}, 400))
    else:
        guesses_allowed = default_guesses_allowed
    
    if 'game_label' in request:
        if len(request['game_label']) > 20:
            abort(make_response({'message': 'game_label must be less than 20 characters.'}, 400))
        else:
            game_label = request['game_label']
    else:
        game_label = None

    return {
        'num_min': num_min,
        'num_max': num_max,
        'code_length': code_length,
        'guesses_allowed': guesses_allowed,
        'game_label': game_label
    }


def generate_number_combo(request):
    code_length = request['code_length']
    num_min = request['num_min']
    num_max = request['num_max']

    path = f'https://www.random.org/integers/?num={code_length}&min={num_min}&max={num_max}&col=1&base=10&format=plain&rnd=new'
    response = requests.get(path)
    response_body = response.text
    num_combo = response_body.replace('\n', '').strip()
    
    return {'num_combo': num_combo, 'num_min': num_min, 'num_max': num_max, 'guesses_allowed': request['guesses_allowed'], 'game_label': request['game_label']}

def validate_guess(guess, game):
    game_dict = game.to_dict()
    guess_str = guess
    try: 
        guess = int(guess)
    except:
        abort(make_response({'message': f'Guess {guess_str} invalid. Guess must be an integer.'}, 400))
    
    if len(guess_str) != len(game_dict['num_combo']):
        abort(make_response({'message': f'Guess {guess_str} invalid. Guess must be {len(game_dict["num_combo"])} digits long.'}, 400))
    elif len(game_dict['guesses']) == game_dict['guesses_allowed']:
        abort(make_response({'message': f'Guess {guess_str} invalid. No more guesses allowed for this game.'}, 400))
    for num in guess: 
        if int(num) not in range(game_dict['num_min'], game_dict['num_max']+1):
            abort(make_response({'message': f'Guess {guess_str} invalid. Each digit in the guess must be between {game_dict["num_min"]} and {game_dict["num_max"]}, inclusive.'}, 400))
    
    guesses = game.guesses_for_game()
    if guess in [guess['guess'] for guess in guesses]:
        abort(make_response({'message': f'Guess {guess_str} invalid. Guess has already been made for this game.'}, 400))

    return {'guess': guess_str, 'game_dict': game_dict}

def calculate_guess_feedback(game_info):
    num_combo = game_info['game_dict']['num_combo']

    guess = game_info['guess']
    
    # if guess = num_combo, game is over
    if guess == num_combo: 
        corr_loc = len(guess)
        corr_num = len(guess)
        return {'game_won': True, 'feedback': f'{corr_num} correct numbers and {corr_loc} correct locations. You guessed the correct code: {num_combo}!', 'corr_loc': corr_loc, 'corr_num': corr_num}

    # tracking if there are repeat numbers
    num_count = collections.defaultdict(int)
    for num in num_combo:
        num_count[num] += 1
    
    corr_loc = 0
    corr_num = 0

    for idx, num in enumerate(guess):
        if num in num_count: 
            num_count[num] -= 1
            if num_count[num] >= 0:
                corr_num += 1
            # can only be in correct location if num is in num_combo
            if num == num_combo[idx]: 
                corr_loc += 1
    
    return {'game_won': False, 'feedback': f'{corr_num} correct number{"s" if corr_num > 1 else ""} and {corr_loc} correct location{"s" if corr_loc > 1 else ""}.', 'corr_loc': corr_loc, 'corr_num': corr_num}

def validate_user(request_body):
    existing_user = User.query.filter_by(username=request_body['username']).count()
    if 'username' not in request_body or 'password' not in request_body:
        abort(make_response({'message': 'Invalid request body. Must include username and password.'}, 400))
    elif existing_user:
        abort(make_response({'message': f'Username ({request_body["username"]}) already exists. Please choose another username.'}, 400))
    return {'username': str(request_body['username']), 'password': str(request_body['password'])}

def validate_login(username, password):

    user = User.query.filter_by(username=username, password=password).first()

    if not user:
        abort(make_response({'message': f'User ({username}) not found. Please check your login credentials or register for an account.'}, 404))

    return user

def generate_hint(game):
    game = game.to_dict()
    last_guess = game['guesses'][-1]['guess']
    num_combo = game['num_combo']
    # hint = 'Hint: r'
    if int(num_combo) > int(last_guess):
        return {'hint': f'The code is greater than your last guess {last_guess}.'}
    else:
        return {'hint': f'The code is less than your last guess {last_guess}.'}

