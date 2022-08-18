import genetic_alg
import rlbot_flappy
#import myQ_flappy_bird
import keyboard

### DRAW BACKGROUND ####

#### DRAW MENU TEXT #####

### IF STATEMENTS FOR INPUT ###

# Import libraires and Classes
import pygame
import os
from Bird import Bird
from Ground import Ground 
# Get font for writing to screen 
pygame.font.init()


#Load images and set size of screen
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

# Load the backgroung image, scale by 2
background_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Set the font for the screen
fonts = pygame.font.SysFont("arial", 30) 

### DRAW THE ANIMATION ###
def draw_window(win, bird, ground): # takes the window and objects to be drawn
    """Draws our objects and Text to the scrren

    Args:
        win (pygame object): window to draw and display
        bird (Custom Class): The bird class to create and move our bird objects
        ground (Custom Class): Ground class to create and move the ground
    """
    win.blit(background_img, (0,0)) # Draw the backgroound at 0, 0

    # Welcome text
    title_text = fonts.render("Welcome to The GA vs DQN!", 1, (255, 255, 255))
    # draw it to the window; use width to keep track of how big the number gets
    win.blit(title_text, (SCREEN_WIDTH * .9  - title_text.get_width(), 50))

    option_text_1 = fonts.render("Press 1 to run GA training", 1, (255, 255, 255))
    # draw it to the window; use width to keep track of how big the number gets
    win.blit(option_text_1, (SCREEN_WIDTH* .9  - option_text_1.get_width(), 100))

    option_text_2 = fonts.render("Press 2 to run best GA bird", 1, (255, 255, 255))
    # draw it to the window; use width to keep track of how big the number gets
    win.blit(option_text_2, (SCREEN_WIDTH * .9  - option_text_2.get_width(), 150))

    option_text_3 = fonts.render("Press 3 to run best adapted Q bird", 1, (255, 255, 255))
    # draw it to the window; use width to keep track of how big the number gets
    win.blit(option_text_3, (SCREEN_WIDTH * .9  - option_text_2.get_width(), 200))

    ground.draw(win)

    # call the draw method from bird and pass it window
    bird.draw(win)
    pygame.display.update() # pygame update method
### DRAW THE WINDOW END ###


#### MAIN LOOP #####
def main_menu():
    """ Main game loop. 
        Will be used to evaluate Bird populations with GA
    """
    bird = Bird(230, 350)  # Create a new bird object 
    ground = Ground(730) # Make the ground
    #pipes = [Pipe(600)] # List of pipes; 600 ideal diffulty after testing
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # create a window object with out width and height
    clock = pygame.time.Clock() # create a clock object to set the ticks per second

    run = True # bool for while loop 
    # Game loop
    while run:
        clock.tick(30) # tick 30 times a second
        for event in pygame.event.get(): # get the events happening via pygame method
            if event.type == pygame.QUIT: # check if we quit the game
                run = False

            # if number 1 pressed, start the genetic Algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    genetic_alg.geneticAlgo() 

            # if number 2 pressed, play best bird from GA
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    local_dir = os.path.dirname(__file__)
                    genetic_alg.replay_genome(os.path.join(local_dir, "config_neat.txt"))

            # if number 1 pressed, start the genetic Algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    rlbot_flappy.game()
                    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

             # if number 1 pressed, start the genetic Algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_4:
                    pass
                    #myQ_flappy_bird.main()


        # Treadmill the ground and draw objects to the window
       
        ground.move()
        draw_window(win, bird, ground)

    # If while loop exited, quit pygame
    pygame.quit()
    quit()

main_menu()
