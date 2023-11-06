
def test_check_user_finds_user(client, user_1):
    response = client.post('/user/authenticate', json={'username': 'test_user', 'password':'password'})
    response_body = response.get_json()
    assert response.status_code == 200
    assert response_body['username'] == 'test_user'
    assert len(response_body['user_games']) == 0
    assert response_body['user_id'] == 1

def test_check_user_returns_error_message_when_not_found(client):
    response = client.post('/user/authenticate', json={'username': 'test_user', 'password':'password'})
    response_body = response.get_json()
    assert response.status_code == 404
    assert 'message' in response_body

def test_create_game_for_user(client, user_1):
    response = client.post('/game', json={'user_id':1})
    assert response.status_code == 201
    
    response_body = response.get_json()
    assert len(response_body['num_combo']) == 4
    assert response_body['num_min'] == 0
    assert response_body['num_max'] == 7
    assert response_body['guesses_allowed'] == 10

    response = client.get('/user/1/games')
    assert response.status_code == 200
    assert len(response.get_json()['games']) == 1

def test_create_game_for_user_returns_error_message_when_user_not_found(client):
    response = client.post('/game', json={'user_id':1})
    assert response.status_code == 404
    assert 'message' in response.get_json()

def test_create_game_with_no_params(client):
    response = client.post('/game', json={})
    assert response.status_code == 201
    
    response_body = response.get_json()
    assert len(response_body['num_combo']) == 4
    assert response_body['num_min'] == 0
    assert response_body['num_max'] == 7
    assert response_body['guesses_allowed'] == 10

def test_create_game_with_params(client):
    response = client.post('/game', json={'num_min': 1, 'num_max': 5, 'code_length': 3, 'guesses_allowed': 5})
    assert response.status_code == 201

    response_body = response.get_json()
    assert len(response_body['num_combo']) == 3
    assert response_body['num_min'] == 1
    assert response_body['num_max'] == 5
    assert response_body['guesses_allowed'] == 5


# 

def test_create_game_with_invalid_params(client):
    response = client.post('/game', json={'num_min': 5, 'num_max': 1, 'code_length': 3, 'guesses_allowed': 5})
    assert response.status_code == 400

    response_body = response.get_json()
    assert 'message' in response_body

def test_create_game_with_invalid_code_length(client):
    response = client.post('/game', json={'num_min': 1, 'num_max': 5, 'code_length': 1, 'guesses_allowed': 5})
    assert response.status_code == 400

    response_body = response.get_json()
    assert 'message' in response_body

def test_create_game_with_invalid_guesses_allowed(client):
    response = client.post('/game', json={'num_min': 1, 'num_max': 5, 'code_length': 3, 'guesses_allowed': 0})
    assert response.status_code == 400

    response_body = response.get_json()
    assert 'message' in response_body

def test_create_game_with_invalid_user_id(client):
    response = client.post('/game', json={'user_id': 999})
    assert response.status_code == 404

    response_body = response.get_json()
    assert 'message' in response_body

def test_get_game_by_id(client, user_1):
    response = client.get(f'/game/1')
    assert response.status_code == 200

    response_body = response.get_json()
    assert response_body['game_id'] == 1
    assert response_body['num_min'] == 0
    assert response_body['num_max'] == 7
    assert response_body['guesses_allowed'] == 10
    assert response_body['game_won'] == False
    assert len(response_body['guesses']) == 0

def test_get_game_by_id_returns_error_message_when_not_found(client):
    response = client.get('/game/999')
    assert response.status_code == 404

    response_body = response.get_json()
    assert 'message' in response_body


def test_get_game_by_id_returns_correct_guesses(client, game_1_with_1_guess):
    response = client.post(f'/game/1/guess', json={'guess': '1234'})
    assert response.status_code == 201
    response_body = response.get_json()
    assert response_body['game_won'] == True


    response = client.get(f'/game/1')
    response_body = response.get_json()
    assert response_body['game_id'] == 1
    assert response_body['num_min'] == 0
    assert response_body['num_max'] == 7
    assert response_body['guesses_allowed'] == 10
    assert response_body['game_won'] == True
    assert len(response_body['guesses']) == 2
    assert response_body['guesses'][0]['guess'] == '1111'
    assert response_body['guesses'][0]['corr_num'] == 0
    assert response_body['guesses'][1]['corr_num'] == 4


def test_make_guess_returns_game_won(client, user_1):
    response = client.post(f'/game/1/guess', json={'guess': '1412'})
    assert response.status_code == 201

    response_body = response.get_json()
    assert response_body['game_won'] == True

