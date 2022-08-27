# Import libraires and Classes
import pygame
import os
import neat
from Bird import Bird
from Pipe import Pipe
from Ground import Ground 
import pickle

### Setting up csv file to write ###
import csv

data = []


#from main_menu import *
# Get font for writing to screen 
pygame.font.init()


#Load images and set size of screen
screen_width = 500
screen_height = 800

# initilize the generations
gen = 0

# Load the backgroung image, scale by 2
background_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Set the font for the screen
fonts = pygame.font.SysFont("arial", 30) 

### DRAW THE ANIMATION ###
def draw_window(win, birds, pipes, ground, score): # takes the window and objects to be drawn
    """Draws our objects and Text to the scrren

    Args:
        win (pygame object): window to draw and display
        bird (Custom Class): The bird class to create and move our bird objects
        pipes (Custom Class): Pipe class to create and move our pipe objects
        ground (Custom Class): Ground class to create and move the ground
        score (int): An int to keep track of the score
    """
    win.blit(background_img, (0,0)) # Draw the backgroound at 0, 0
    # Loop for pipes
    for pipe in pipes:
        pipe.draw(win)

    # Set up our text for score
    text = fonts.render("Score: " + str(score), 1, (255, 255, 255))
    # draw it to the window; use width to keep track of how big the number gets
    win.blit(text, (screen_width - 10 - text.get_width(), 10))

    ground.draw(win)

    for bird in birds:
        bird.draw(win) # call the draw method from bird and pass it window
    pygame.display.update() # pygame update method
### DRAW THE WINDOW END ###


#### MAIN LOOP - Rename to eval_pop #####
def eval_genomes(genomes, config): # we pass it genomes and the config object to run the GA
    nets = [] # neural network for each bird
    ge = [] # geneomes for birds
    birds = []  # Create a new bird list

    global  gen
    gen += 1

    #### NEURAL NETWORK SET UP CODE ###
    # Set up genomes and neural networks
    for _, g in genomes: # need the _ because genomes is a tupple genome id and genome object -> (1, genome)
            net = neat.nn.FeedForwardNetwork.create(g, config) # set up neural network
            nets.append(net) # add to our list
            birds.append(Bird(230, 350)) # add new bird to the list
            g.fitness = 0 # initialize the fitness of this population to 0
            ge.append(g) # add the genome to the list

    #### END NEURAL NETWORK SET UP CODE ####

    ground = Ground(730) # Make the ground
    pipes = [Pipe(600)] # List of pipes; 600 ideal diffulty after testing
    win = pygame.display.set_mode((screen_width, screen_height)) # create a window object with out width and height
    clock = pygame.time.Clock() # create a clock object to set the ticks per second

    score = 0 # Keep track of that score

    run = True # bool for while loop 

    # Game loop
    while run:
        clock.tick(30) # tick 30 times a second
        for event in pygame.event.get(): # get the events happening via pygame method
            if event.type == pygame.QUIT: # check if we quit the game
                run = False
                break
                #pygame.quit()
                #quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
                    #print("Escape")
        


        ##### NEURAL NETWORK NEAT CODE #####
        ### Deciding which pipe the birds should be looking at ###
        pipe_ind = 0 # Start with an index of 0
        if len(birds) > 0:
            # if the bird is past the first pipe look at the second
            # (there shouldn't be more than two pipes on the screen)
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].top_pipe.get_width():
                pipe_ind = 1
            # Othrwise we have no more birds
        else:
            run = False
            # out put the score and the generation when a population dies
            print("Score: " + str(score), "Generation: " + str(gen))
            break

        for x, bird in enumerate(birds):
            bird.move()
            #add fitness if still alive
            ge[x].fitness += 0.1

            # creates a list that holds the value of output from a neural network
            # config file is set up with only 1, but more can be added
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            # If the neuron is activated more than 0.5, jump
            if output[0] > 0.5:
                bird.jump()

        # keep track of if we need to add a pipe or not
        add_pipe = False


        # Iterate through the pipes, and move them
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -=1 # lower the fitness of the bird
                    birds.pop(x) # (un)natural selection; bird killed
                    nets.pop(x) # remove the birds brain
                    ge.pop(x) # remove the genome


                # Check if bird has passed the pipe
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            # Check if pipe moved off screen and remove
            if pipe.x + pipe.top_pipe.get_width() < 0:
                pass
            
            # Move the pipes forward
            pipe.move()

        # If we passed a pipe add to score and add a new point
        if add_pipe:
            score += 1
            for g in ge: # add to the fitness of the birds who made it
                g.fitness +=5
            pipes.append(Pipe(600))

            # Remove pipes from pipe list 
            # For now removes if pipes list is greater than 2
            # Later change to if they are off screen
            if len(pipes) > 2:
                pipes.pop(0)
        
        # Check if bird has hit the ground or goes above screen
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x) # remove bird
                nets.pop(x) # remove nerual network
                ge.pop(x) # remove genome

        if score >= 1000:
            run = False
            break

        # Move the ground, draw the window
        ground.move()
        draw_window(win, birds, pipes, ground, score)

    #print(gen, score)
    data.append([gen, score])


def run(config_path):
    # Takes the configuration file and builds the neural network based on
    # The paramters we set 
    config = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, 
                                neat.DefaultStagnation, 
                                config_path)

    # population
    p = neat.Population(config)

    # Output/data on the populations performance
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter() #StatisticsReporter
    p.add_reporter(stats)
    
    # Runs NEAT’s genetic algorithm for at most n generations and save the winner
    winner = p.run(eval_genomes, 5)

    # Get the previous winner
    with open("winner.pkl", "rb") as f:
        prev_winner = pickle.load(f)
        f.close
    
    # If the new winner did better, save him
    if prev_winner.fitness < winner.fitness:
        print("New Winner!!")
        with open("winner.pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close()

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

def replay_genome(config_path, genome_path="winner.pkl"):
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    eval_genomes(genomes, config)
    

def geneticAlgo():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_neat.txt")
    run(config_path)

    header = ['Generation', 'Score']

    with open('Scores.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)

        # write the header
        writer.writerow(header)
        writer.writerows(data)
        file.close() 

   
