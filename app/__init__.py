from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
import os # used to get the variables from the .env file for the database connection

db = SQLAlchemy()
migrate = Migrate()
load_dotenv() #will make available as env variables and for teh system to use

def create_app(testing=None):
    app = Flask(__name__)
    CORS(app)
    
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if testing is None: 
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else: 
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')



    #establish models 
    #import pattern for models
    # will need to run flask db migrate and flask db upgrade to create the tables in the database


    #only boards we will be storing will be the daily challenge boards 
    # will also create a model for the leaderboard and users
    from app.models.game import Game
    from app.models.guess import Guess
    from app.models.user import User

    db.init_app(app)
    migrate.init_app(app,db)

    #establish blueprints - need to update these variables blueprint -> board, etc
    from app.routes.game import game_bp
    from app.routes.user import user_bp
    app.register_blueprint(game_bp)
    app.register_blueprint(user_bp)
    
    return app