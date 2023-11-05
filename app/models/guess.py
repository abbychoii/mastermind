from app import db
from datetime import datetime

# Guess model representing individual guesses by users (many to one relationship with games)

class Guess(db.Model):
    guess_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guess = db.Column(db.String(10), nullable=False)
    game_id = db.Column(db.Integer,db.ForeignKey('game.game_id'), nullable=False)
    game = db.relationship("Game", back_populates="guesses")
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    corr_num = db.Column(db.Integer, nullable=False)
    corr_loc = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String, nullable=False)

    def to_dict(self):
        guess_dict = {
            'guess_id': self.guess_id,
            'game_id': self.game_id,
            'guess': self.guess,
            'num_combo': self.game.num_combo,
            'created_at': self.created_at,
            'corr_num': self.corr_num,
            'corr_loc': self.corr_loc,
            'feedback': self.feedback,
            'game_won': self.game.game_won,
        }
        return guess_dict 
    
    @classmethod
    def from_dict(self, request):
        guess = Guess(
            guess=request['guess'],
            game_id=request['game_id'],
            corr_num=request['corr_num'],
            corr_loc=request['corr_loc'], 
            feedback=request['feedback']
        )
        return guess