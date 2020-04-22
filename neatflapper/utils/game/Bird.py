from neatflapper.utils import Resources
import pygame
import numpy as np
from pythonneat.nn.FeedForwardNetwork import FeedForwardNetwork
import pythonneat.utils.Activations as Activations


def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotate a surface and blit it to the window
    :param surf: the surface to blit to
    :param image: the image surface to rotate
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)


class Bird:
    IMGS = Resources.BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.network = FeedForwardNetwork(6)
        self.network.layer(3, act_func=Activations.tanh)
        self.network.layer(1)
        self.score = 0
        self.next_pipe = None

    def act(self, pipes):
        self.next_pipe = pipes[0]
        if self.next_pipe.passed:
            self.next_pipe = pipes[1]

        out = self.network.forward_propagate(np.array([Resources.get_bird_mid(self)[0],
                                                       Resources.get_bird_mid(self)[1],
                                                       Resources.get_pipe_top_mid(self.next_pipe)[0],
                                                       Resources.get_pipe_top_mid(self.next_pipe)[1],
                                                       Resources.get_pipe_bottom_mid(self.next_pipe)[0],
                                                       Resources.get_pipe_bottom_mid(self.next_pipe)[1]]))

        if out[0] >= 0.5:
            self.vel = -10.5
            self.tick_count = 0
            self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16
        elif d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, window):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        blitRotateCenter(window, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
