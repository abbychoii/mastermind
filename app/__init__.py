from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
import os 

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(testing=None):
    app = Flask(__name__)
    

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if testing is None:
        uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = uri
    else:
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')

    

    #establish models 
    #import pattern for models
    # will need to run flask db migrate and flask db upgrade to create the tables in the database

    #create models for Game, Guess, User
    from app.models.game import Game
    from app.models.guess import Guess
    from app.models.user import User

    db.init_app(app)
    migrate.init_app(app,db)

    from app.routes.game import game_bp
    from app.routes.user import user_bp
    app.register_blueprint(game_bp)
    app.register_blueprint(user_bp)
    
    CORS(app)
    return app