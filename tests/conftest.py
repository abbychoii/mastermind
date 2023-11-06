import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.user import User
from app.models.game import Game
from app.models.guess import Guess

@pytest.fixture 
def app():
    app = create_app({'TESTING': True})
    
    @request_finished.connect_via(app)
    def expire_session(sender,response,**extra):
        db.session.remove()
    
    with app.app_context(): 
        db.create_all()
        yield app
        # yield will give app object and continue to run the code in the function until seeing db.session.remove or db.drop_all(). will only be used in context of testing
    
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture 
def user_1(app):
    user1 = User(username='test_user', password='password')
    game1 = Game(user_id=user1.user_id,num_combo='1412',num_min=0, num_max=7, guesses_allowed=10)
    
    db.session.add(user1)
    db.session.add(game1)

    db.session.commit()
    return user1

@pytest.fixture
def game_1_with_1_guess(app):
    game1 = Game(num_combo='1234', num_min=0, num_max=7, guesses_allowed=10)
    db.session.add(game1)

    guess1 = Guess(game_id=1, guess='1111', corr_num=0, corr_loc=0, feedback='0 correct number and 0 correct location.')

    db.session.add(guess1)
    db.session.commit()
    return game1