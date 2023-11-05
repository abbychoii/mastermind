from app import db

# Game model representing individual games by users (many to one relationship with users)
class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    game_label = db.Column(db.String(20), nullable=False, default="Game {game_id}")   
    # need to store the allowed range to validate guesses based off preset range
    num_min = db.Column(db.Integer, default=0, nullable=False)
    num_max = db.Column(db.Integer, default=7, nullable=False)
    # don't need to store the length because the num_combo will be of the correct length, but the range might not be fully reflected in the num_combo (so need to store the range)
    num_combo = db.Column(db.String(10), nullable=False)
    guesses = db.relationship("Guess", back_populates="game", lazy=True)
    guesses_allowed = db.Column(db.Integer, nullable=False, default=10)# can be empty - if empty then game is still in progress
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    game_won = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'game_id': self.game_id,
            'game_label': self.game_label,
            'num_combo': self.num_combo,
            'num_min' : self.num_min,
            'num_max' : self.num_max,
            'guesses_allowed' : self.guesses_allowed,
            'game_won' : self.game_won,
            'guesses': self.guesses_for_game(),
            'date_created': self.date_created.strftime("%Y-%m-%d %H:%M")
        }
    def guesses_for_game(self):
        return [guess.to_dict() for guess in self.guesses]
    
    @classmethod
    def from_dict(cls, request):
        game = Game(
            user_id=request.get('user_id'),
            num_min=request['num_min'],
            num_max=request['num_max'],
            num_combo=request['num_combo'],
            guesses_allowed=request['guesses_allowed'], 
            game_label=request['game_label'])
        return game