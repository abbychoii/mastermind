def test_check_guess_with_empty_guess_returns_400(client):
    response = client.get('/guess', json={'guess':'', 'combo': '1234'})
    response_body = response.get_json()

    #400 bad request
    assert response.status_code == 400
    assert 'message' in response_body

def test_check_guess_with_empty_combo_returns_400(client):
    response = client.get('/guess', json={'guess':'1234', 'combo': ''})
    response_body = response.get_json()

    assert response.status_code == 400
    assert 'message' in response_body

# all guesses.length == combo.length (also each digit must be within the preset range of 0-7)
def test_check_guess_with_invalid_guess_length_returns_400(client):
    response = client.get('/guess', json={'guess':'12345', 'combo': '1234'})
    response_body = response.get_json()

    assert response.status_code == 400
    assert 'message' in response_body

def test_check_guess_with_invalid_guess_digit_returns_400(client):
    response = client.get('/guess', json={'guess':'1239', 'combo': '1234'})
    response_body = response.get_json()

    assert response.status_code == 400
    assert 'message' in response_body