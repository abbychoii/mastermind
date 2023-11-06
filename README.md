# Mastermind

Flask backend server for the mastermind game to handle code generation and verify guesses. The backend server is deployed and being utilized to support the [Mastermind](https://masterminds-9a215e501a94.herokuapp.com/) site.
* [Frontend Repo](https://github.com/abbychoii/mastermind-site)
  * main branch - deployed at [Mastermind](https://masterminds-9a215e501a94.herokuapp.com/)
  * mastermind local branch - local build (contains links that align with running front & backend locally)
* [Backend Repo](https://github.com/abbychoii/mastermind)
* [Command Line Script](https://github.com/abbychoii/mastermind-cl)


## Running the Flask Server Locally
### Create virtual environment
Navigate to the project directory (cd mastermind): 
```console 
## create a virtual environment
python3 -m venv venv

## activate virtual environment
source venv/bin/activate 

## install packages
pip install -r requirements.txt

## when deactivating virtual environment: 
deactivate
```

### Create Databases
PostgreSQL was used for the database in this project. 
```console
createdb mastermind
```
### .env file to connect to database 
Create a .env file in the mastermind folder and enter the following: 
`SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/mastermind`
  * Depending on what port is used, 5432 may be a different number 
  * If you name the database something other than mastermind, then mastermind should be changed to the database name!7

### Run Flask Server 
Apply migrations to database: <br>
`flask db upgrade`    
Navigate to project folder (mastermind) <br>
`flask run`

### Tests
Tests can be run using the command `pytest tests/test_routes.py` from the mastermind folder. 

## Project Direction 
### MVP
I originally started with a [command line python script](https://github.com/abbychoii/mastermind-cl) that I used to step through what things I needed to consider to implement this game. I focused on how to calculate the number of correct digits and location in the code, as well as input validation (checking for valid guesses). I wanted to make the game a little more user friendly, thus, created this site that can be used to play the game. 

The primary focus was completing the MVP of a relatively simple site that would include a way to generate a random number combination and a way to submit guesses and receive feedback. The game was implemented for a single player. 

### Additional Features
1. Customizable difficulty levels, including 3 presets
   1. Easy (4 digit code, 10 guesses)
   2. Medium (5 digit code, 10 guesses)
   3. Hard (6 digit code, 10 guesses)
   4. Custom (2-10 digit code, 2-20 guesses)
2. Option to login/create a user profile that can save the games played and allow you to continue unfinished games
3. Providing hints to help users get closer to the code! 

### Backend Design & Considerations
As this was a relatively lightweight application, I utilized PostgreSQL, Flask and SQLAlchemy for the backend of this project. The backend for mastermind consists of 3 tables: Games, Guesses, and User. Originally, I only implemented the Game model, developing the other models later as I began extending the functionality of the site. 

I wanted to provide greater flexibility in ways to utilize the API, consequently, even though Mastermind is typically a game breaking a 4 digit code with digits in the range of 0 to 7, the backend supports a wider range of options. A game is able to be generated with a length ranging from 2-10 digits, with each digit in the range of 0-9. Additionally, you are able to customize the number of guesses allowed. 

### Models 
1. Game Model (Game Table)
   * stores information about the game's combination (num_combo), as well as what parameters were utilized in the generation of the num_combo (num_min, num_max, date_created, game_won)
     * With random number generation, the digits in the number combination are not reflective of all allowed inputs so these values were stored separately in (num_min, num_max, storing the range that was allowed for that game)
   * Games have a one to many relationship with guesses, with guesses having to be associated with a game.
   * Users have a one to many relationship with Games. To support the greatest flexibility though, games do not have to be associated with a user (can have the foreign key be None)
2. Guess Model (Guess Table)
   * stores information about guesses for the game, including the guess value, how many correct digits are included and how many are in the correct location
     * I originally returned a feedback string directly, but added the corr_num and corr_loc values so that they can be displayed as desired within the frontend.
     * each guess is associated with a game and cannot be added to the database without an existing relationship to a game
3. User Model (User Table)
   * I wanted to add a way for users to see their game history, see what games they've won/lost, and also be able to continue unfinished games 
   * created a user model that stores a user's username, password, and their games

### Routes 
The routes folder consists of the API endpoints, with routes_helper consisting of helper functions for input validation and external api calls to the random number generator. 
1. User Routes
   * endpoints support creating a user
   * logging in a user (validating that user exists, username and password are correct)
   * getting a user's information (username, id, games)
   * all the games belonging to a user (games from user_id)
2. Games Routes 
   * endpoints for creating a game
   * creating a guess (guess must be associated with a game)
   * getting a game from a game_id
   * getting all guesses for a game from the game_id
   * getting a hint based off of last guess made for a game