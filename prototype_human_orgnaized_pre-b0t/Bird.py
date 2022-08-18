import pygame
import os

# Globals for classes
# Load the bird images, scale by 2
bird_imgs = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]


###### Bird Class ########
class Bird:
    imgs = bird_imgs
    max_rot = 25 # Maximum degrees, guessed by watching old videos of flappy bird
    rot_vel = 20 # Rotation velocity how much to rotate the bird each frame 
    animation_speed = 5 # How fast the bird will "flap"

    ###### INITALIZE THE BIRD #######
    def __init__(self, x, y):
        self.x = x #starting x coordinate
        self.y = y #starting y coordinate
        self.tilt = 0 #starting tilt, we are looking straigt ahead
        self.tick_count = 0 # used to help with physics of gravity
        self.vel = 0 #velocity
        self.height = self.y # used seperatly from y for moving and tilting the bird
        self.img_count = 0 #which image we are curretnly using to animate(i.e straigt, tilt etc.)
        self.img = self.imgs[0] #referencing out array of loaded bird images
    ###### INITALIZE THE BIRD END #######

    #### JUMP METHOD ###
    def jump(self):
        """
            Move the bird upward on the y axis
        """
        self.vel = -10.5 #Used for jumping, number was tested from various till one looked right
        self.tick_count = 0 # keep track of when we last jumped
        self.height = self.y # where the bird jumped from
    #### JUMP METHOD END ###

    #### MOVE METHOD #####
    def move(self):
        """ Controls the gravity effect on the bird, terminal velocity
            displacement and tilt of the bird when moving
        """
        self.tick_count += 1 # a frame happened and we moved
        #displacement - how many pixels(up or down) we moved this frame
        # Formula for displacement - velocity times time plus 1/2 times accelration squared
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2

        # set a "terminal velocity" to not exceed
        if d >= 16:
            d = 16

        # added to smooth out the jumping; number chosen by testing a few others at random
        if d < 0:
            d -= 2

        # update our y position based on displacement above
        self.y = self.y + d 

        # check if we are moving up and tilt the bird up
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.max_rot: # Make sure we aren't over tilting and looking weird
                self.tilt = self.max_rot

        # If we are falling down, then nose down to the ground
        else:
            if self.tilt > -90:
                self.tilt -= self.rot_vel
    #### MOVE METHOD END #####

    #### DRAW THE BIRD METHOD ####
    def draw(self, win): # takes self and the window to draw onto
        """Draws the bird to the screen 

        Args:
            win (pygame object): window the picutrew will be drawn to
        """
        self.img_count += 1 # keep track for how long image has been shown

        # check and cycle through the images displayed after every 5 count
        if self.img_count < self.animation_speed:
            self.img = self.imgs[0]
        elif self.img_count < self.animation_speed * 2:
            self.img = self.imgs[1]
        elif self.img_count < self.animation_speed * 3:
            self.img = self.imgs[2]
        elif self.img_count < self.animation_speed * 4:
            self.img = self.imgs[1]
        elif self.img_count == self.animation_speed * 4 + 1:
            self.img = self.imgs[0]
            self.img_count = 0

        # when bird is tilted, don't flap wings
        if self.tilt <= -80:
            self.img = self.imgs[1]
            # when bird jumps up tranisiton the imags smoothly
            self.img_count = self.animation_speed * 2

        # rotate and tilt the image effect, pygame inbuilt funciton
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # set the point of rotation to be the center
        # found on stack overflow
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        # draw the image
        win.blit(rotated_image, new_rect.topleft)
    #### DRAW THE BIRD METHOD END ####

    #### GET MASK FOR COLLISION DETECTION METHOD #### 
    def get_mask(self):
        """Gets the "mask" - an object represnting the 2D bitmask
           Used for pixel perfect collison

        Returns:
            mask: pygame object
        """
        return pygame.mask.from_surface(self.img)
    ####GET MASK FOR COLLISION DETECTION METHOD END ####
#### Bird Class End ####