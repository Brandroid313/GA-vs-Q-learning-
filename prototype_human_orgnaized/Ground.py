import pygame
import os

# Globals for classes
# Load the ground image, scale by 2
ground_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

#### Ground Class #####
class Ground:
    """Creates the scrolling Ground
    """
    # Constants
    speed = 5 # Velocity of ground moving, same as pipes
    width = ground_img.get_width() # width of ground, same as width of ground image
    img = ground_img # the imgage of the ground itself 

    # Methods


    def __init__(self, y):
        self.y = y # height
        self.x1 = 0 # ground 1, for illusion of infinite ground
        self.x2 = self.width # ground 2, for illusion of infinite ground

    #### MOVING GROUND METHOD ####
    def move(self):
        """
            Moves the ground likea tread mill
            By replaceing the ground in front with ground behind
        """
        # move both grounds to the left at the same speed
        self.x1 -= self.speed
        self.x2 -= self.speed

        # Cycles the ground images; as one is going off screen, another will replace it
        # when the first one is completely offscreen, move it to behind the second
        # rinse repeat
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width
    #### MOVING GROUND METHOD END ####


    #### DRAW THE GROUND METHOD ####
    def draw(self, win):
        """Draws the ground at two x points

        Args:
            win (pygame window): Takes the win argument used to call blit
            *Blit is the pygame function to draw to the screen
        """
        win.blit(self.img, (self.x1, self.y)) # draw the first ground onscreen
        win.blit(self.img, (self.x2, self.y)) # draw the second ground just offscreen
    #### DRAW THE GROUND METHOD ####
#### Ground Class End #####