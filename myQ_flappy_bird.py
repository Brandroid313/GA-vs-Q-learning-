# Import libraires and Classes
import pygame
import os
from Bird import Bird
from Pipe import Pipe
from Ground import Ground 
from qbot import Bot
import datetime
# Get font for writing to screen 
pygame.font.init()

#### BOT STUFFF #######
bot = Bot()
def getNextUpdateTime():
    return datetime.datetime.now() + datetime.timedelta(minutes = 1)

NEXT_UPDATE_TIME = getNextUpdateTime()

#### END BOT STUFFF 

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


##### Q TABLE BOT STUFF #########


def updateQtable(score):
    global NEXT_UPDATE_TIME

    justUpdate = False
    if  datetime.datetime.now() > NEXT_UPDATE_TIME or score > 100:
        bot.dump_qvalues(force=True)
        justUpdate = True
        NEXT_UPDATE_TIME = getNextUpdateTime()

    
    # if bot.gameCNT >= EPISODE:
    #     if not justUpdate: bot.dump_qvalues(force=True)
    #     showPerformance()
    #     pygame.quit()
    #     sys.exit()

#####END Q TABLE BOT STUFF #########

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

    # first_jump = True

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
        bird.move()

    
        # Iterate through the pipes, and move them
        for pipe in pipes:

            if pipe.collide(bird):
                # Restart the game if collision 
                #print("Collision!")
                print("Game " + str(bot.gameCNT+1) + ": reach " + str(score) + "...")
                bot.update_scores(died=True)
                updateQtable(score)

                main()

                # run = False
                # break

                # pygame.quit()
                # quit()

            if bot.act(bird.x, bird.y, bird.vel, pipes):
                bird.jump() 
            
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
            bot.update_scores(died = False, score=True)
            pipes.append(Pipe(600))

        
        
        # Check if bird has hit the ground
        if bird.y + bird.img.get_height() >= 730:
            print("Game " + str(bot.gameCNT+1) + ": reach " + str(score) + "...")
            bot.update_scores(died = True)
            updateQtable(score)
            #run = False

            main()

            # run = False
            # break

            # pygame.quit()
            # quit()

         # Check if bird has hit the ground
        if bird.y + bird.img.get_height() < 0:
            print("Game " + str(bot.gameCNT+1) + ": reach " + str(score) + "...")
            bot.update_scores(died = True)
            updateQtable(score)
            #run = False

            main()

            # run = False
            # break

            # pygame.quit()
            # quit()

        # Treadmill the ground and draw objects to the window
        ground.move()
        draw_window(win, bird, pipes, ground, score)

    # If while loop exited, quit pygame
    pygame.quit()
    #quit()


#### MAIN LOOP #####
def noui():
    """ Main game loop. 
        Will be used to evaluate Bird populations with GA
    """
    bird = Bird(230, 350)  # Create a new bird object 
    ground = Ground(730) # Make the ground
    pipes = [Pipe(600)] # List of pipes; 600 ideal diffulty after testing
    win = pygame.display.set_mode((screen_width, screen_height)) # create a window object with out width and height
    clock = pygame.time.Clock() # create a clock object to set the ticks per second

    score = 0 # Keep track of that score

    # first_jump = True

    run = True # bool for while loop 
    # Game loop
    while run:
        clock.tick(3000) # tick 30 times a second

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
        bird.move()

    
        # Iterate through the pipes, and move them
        for pipe in pipes:

            if pipe.collide(bird):
                # Restart the game if collision 
                #print("Collision!")
                print("Game " + str(bot.gameCNT+1) + ": reach " + str(score) + "...")
                bot.update_scores(died=True)
                updateQtable(score)

                #main()

                run = False
                break

                # pygame.quit()
                # quit()

            if bot.act(bird.x, bird.y, bird.vel, pipes):
                bird.jump() 
            
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
            bot.update_scores(died = False, score=True)
            pipes.append(Pipe(600))

        
        
        # Check if bird has hit the ground
        if bird.y + bird.img.get_height() >= 730:
            print("Game " + str(bot.gameCNT+1) + ": reach " + str(score) + "...")
            bot.update_scores(died = True)
            updateQtable(score)
            #run = False

            #main()

            run = False
            break

            # pygame.quit()
            # quit()

         # Check if bird has hit the ground
        if bird.y + bird.img.get_height() < 0:
            print("Game " + str(bot.gameCNT+1) + ": reach " + str(score) + "...")
            bot.update_scores(died = True)
            updateQtable(score)
            #run = False

            #main()

            run = False
            break

            # pygame.quit()
            # quit()

        # Treadmill the ground and draw objects to the window
        ground.move()
        #draw_window(win, bird, pipes, ground, score)

    # If while loop exited, quit pygame
    pygame.quit()
    #quit()

main()

# for i in range(1000):
#     noui()

#quit()

# for i in range(5):
#     main()
