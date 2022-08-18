# Import libraires and Classes
import pygame
import os
from Bird import Bird
from Pipe import Pipe
from Ground import Ground
#from qbot import Bot 
# Get font for writing to screen 
pygame.font.init()


#Load images and set size of screen
screen_width = 500
screen_height = 800


# Load the backgroung image, scale by 2
background_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Set the font for the screen
fonts = pygame.font.SysFont("arial", 30) 

### DRAW THE ANIMATION ###
def draw_window(win, bird, pipes, ground, score): # takes the window and objects to be drawn
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

    bird.draw(win) # call the draw method from bird and pass it window
    pygame.display.update() # pygame update method
### DRAW THE WINDOW END ###


#### MAIN LOOP #####
def main():
    """ Main game loop. 
        Will be used to evaluate Bird populations with GA
    """
    bird = Bird(230, 350)  # Create a new bird object 
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
            # detect if space bar was pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump() 

        
        # keep track of if we need to add a pipe or not
        add_pipe = False

        # Apply gravity to the bird, animate wings and control rotation
        #bird.move()

        # Iterate through the pipes, and move them
        for pipe in pipes:
            if pipe.collide(bird):
                # Restart the game if collision
                #main()
                pass

            # Check if pipe moved off screen and remove
            if pipe.x + pipe.top_pipe.get_width() < 0:
                pipes.pop(0)
                
            # Check if bird has passed the pipe
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        # If we passed a pipe add to score and add a new point
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        
        # Check if bird has hit the ground
        if bird.y + bird.img.get_height() >= 730:
           # main()
           pass

        # Treadmill the ground and draw objects to the window
        ground.move()
        draw_window(win, bird, pipes, ground, score)

    # If while loop exited, quit pygame
    pygame.quit()
    quit()

main()
