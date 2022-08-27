# GA versus Q learning 
Welcome to my final year project. Please find below some information if your want to tinker with this project

# To Run
The code is set up in a virtual environment that should be inlcuded in this repo and should already contain the dependancies below. To run type source MyEnv/bin/activate

## Run the main program
From the Terminal in the root folder, type python main_menu.py From there you can select which of the GA training, GA best bird, Q-learning trianing/best ( same program ) and a third party flappy bird q-learning program that mine was based off of ( <https://github.com/chncyhn/flappybird-qlearning-bot> ) 

# Dependancies
- python 3.7
- NEAT 
- pygame

# Main Files
- main_menu.py This is the menu where the different agents and training can be accessed
- myQ_flappy_bird.py The flappy bird game adapted for the q-learning bot
- qbot.py My attempt at building a q-learning agent
- config_neat.txt The configuration file for the GA's inital genomes
- genetic_alg.py The implementation of the GA using the NEAT library
- rlbot_flappy.py and bot.py The implmentation from chncyhn

# Support Files
-data This file is for the implementation of q-learning by chncyhn
- imga The images of the birds, pipes, background and pipes
- MyEnv The virutal environment, already set up (hopefully) for running this project so others can just plug and play


# Credits 
-The q learning bot ( under myQ_flappy_bird.py and q_bot ) was inspired by the worl found here <https://github.com/chncyhn/flappybird-qlearning-bot>

- The main flappy bird game was adapted from the code here <https://github.com/alessandraburckhalter/Flappy-Bird-Pygame/blob/master/game.py>

- The implementation of the GA was inspired by and adapted from the code here <https://github.com/techwithtim/NEAT-Flappy-Bird>

