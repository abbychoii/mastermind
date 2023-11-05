import pytest
from app import create_app
from app import db
from flask.signals import request_finished

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

