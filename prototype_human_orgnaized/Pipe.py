import pygame
import random
import os

#fonts = pygame.font.SysFont("arial", 30) 
# Globals for classes
#Load the pipe images, scale by 2
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))

#### Pipe Class ####
class Pipe:
    # Constants
    pipe_gap = 200 # space between pipes
    velocity = 5 # speed our pipes move towards birds

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.fonts = pygame.font.SysFont("arial", 30)

        self.top = 0 # Keep track where the top of the pipe is drawn
        self.bottom = 0 # keep track where the bottom is going to be drawn
        self.top_pipe = pygame.transform.flip(pipe_img, False, True) # Reuse the bottom image and flip it to be a top
        self.bottom_pipe = pipe_img # Bottom is the image loaded

        # has bird passed by pipe
        self.passed = False

        # set the length/height of the pipes
        self.set_height()

    #### METHOD TO RANDOMLY SET THE LENGTH/HEIGHT OF THE PIPES ####
    def set_height(self):
        """
            Sets the height randomly for the pipes
        """
        self.height = random.randrange(40, 450)

        # Get the top pipes height to be drawn
        self.top = self.height - self.top_pipe.get_height()
        self.bottom = self.height + self.pipe_gap
    #### METHOD TO RANDOMLY SET THE LENGTH/HEIGHT OF THE PIPES END ####

    ##### MOVE THE PIPES ####
    def move(self):
        """
            moves the pipes from right to left by
            subtracting velocoty from the x value    
        """
        self.x -= self.velocity
    ##### MOVE THE PIPES END ####

    #### METHOD TO DRAW PIPES ####
    def draw(self, win):
        """Draws the pipes to the window

        Args:
            win (pygame object): window that will be drawn to
        """
        win.blit(self.top_pipe, (self.x, self.top))
        win.blit(self.bottom_pipe, (self.x, self.bottom))
        # Set up our text for score
        text = self.fonts.render(str(self.bottom), 1, (255, 255, 255))
    # draw it to the window; use width to keep track of how big the number gets
        win.blit(text, (self.x, abs(self.bottom - self.pipe_gap)))

        # bottom rim = self.bottom
        # top_rim = self.bottom - self.pipe_gap
    #### METHOD TO DRAW PIPES END ####

    #### COLLISION DETECTION METHOD ####
    def collide(self, bird):
        """Detects collision, returns True if detected, Falst othersie

        Args:
            bird (Bird class object): Bird object

        Returns:
            Bool: True if collision detected, False otherwise
        """

        # get the maks ( a way of detecting pixels inside bounding/collsion boxes)
        bird_mask = bird.get_mask() # get bird mask
        top_mask = pygame.mask.from_surface(self.top_pipe) # get top mask
        bottom_mask = pygame.mask.from_surface(self.bottom_pipe) # get bottom mask

        # calculate offset (distance of masks from each other)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # check if the masks are colliding
        b_point = bird_mask.overlap(bottom_mask, bottom_offset) # checks collsion of bird and bottom pipe; returns None or a number
        t_point = bird_mask.overlap(top_mask, top_offset) # checks collsion of bird and top pipe

        # if bottom point or top point are not none (a collision)
        if b_point or t_point:
            return True

        return False
    #### COLLISION DETECTION METHOD ####
#### Pipe Class End ####