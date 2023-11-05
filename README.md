# Mastermind

Flask backend server for the mastermind game to handle code generation and verify guesses. 

## Create virtual environment
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

## Create Databases
PostgreSQL was used for the database in this project. 


## Run Flask Server 


## MVP - Minimum Viable Product 
The Integer Generator API will be utilized to generate the number combinations depending on the requested length and range. 

## Stretch Goals 
1. Create a database that will store the daily challenge boards (number and color), and will also keep track of users who have succeded guessing correctly (will be ranked on how many guesses + how long it took!)
   1. Will create a model for the challenge board (number combination)
      1. Challenge board will store the leaderboard that will hold the users
   2. Will create a model for users (which will be stored on the leaderboard)
2. Create a way to make the game multiplayer (2-player)
   1. If multiplayer - create an id/code that can be used to access the board (number combination)
      1. Need to determine whether users will be allowed to create their own board? -> if creating their own board, will verify the code and store the code in a database 
      2. will create a model of users and each game will store whether single or multiplayer 
         1. if multiplayer will have two boards and two users 
         2. if single player will have singular board and 1 user
