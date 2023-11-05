from app import db
# backref - declares new property on the Game class
# lazy - defines when SQLAlchemy will load the data from the database

# User represents users of the game (one-to-many relationship with Game model - one user can have many games)
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    games = db.relationship('Game', backref='user', lazy=True)
    
    #not returning the password
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'user_games': [game.to_dict() for game in self.games]
        }

    @classmethod
    def from_dict(cls, request_body):
        user = User(
            username=request_body['username'],
            password=request_body['password']
        )
        return user
