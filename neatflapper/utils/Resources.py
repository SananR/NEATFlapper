import pygame
import os

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "background.png")))


def get_bird_mid(bird):
    out = (bird.x + (bird.IMGS[0].get_width() / 2), bird.y + (bird.IMGS[0].get_height() / 2))
    return out


def get_pipe_bottom_mid(pipe):
    out = (pipe.x + (PIPE_IMG.get_width() / 2), pipe.bottom)
    return out


def get_pipe_top_mid(pipe):
    bot = get_pipe_bottom_mid(pipe)
    out = (bot[0], bot[1] - 200)
    return out
