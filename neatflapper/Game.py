import pygame
from neatflapper.utils.game.Bird import Bird
from neatflapper.utils.game.Base import Base
from neatflapper.utils.game.Pipe import Pipe
from neatflapper.utils import Resources


PIPE_GAP = 400
PIPE_START_GAP = 500

WIN_WIDTH = 500
WIN_HEIGHT = 800
BASE_HEIGHT = WIN_HEIGHT - 100

BIRD_START_X = 200
BIRD_START_Y = 200

BIRDS = []
PIPES = []


def draw_window(window, base):
    window.blit(Resources.BG_IMG, (0, 0))
    for bird in BIRDS:
        bird.draw(window)
    for pipe in PIPES:
        pipe.draw(window)
    base.draw(window)
    pygame.display.update()


def handle_pipes():
    for pipe in PIPES:
        pipe.move()
        if pipe.x + Resources.PIPE_IMG.get_width() < 0:
            PIPES.remove(pipe)
        if not pipe.passed and pipe.x < BIRD_START_X:
            pipe.passed = True
            PIPES.append(Pipe(PIPES[len(PIPES) - 1].x + PIPE_GAP))


def handle_birds():
    for bird in BIRDS:
        bird.act()
        bird.move()
        if PIPES[0].collide(bird):
            BIRDS.remove(bird)
        elif bird.y + bird.img.get_height() >= WIN_HEIGHT or bird.y + bird.img.get_height() <= 0:
            BIRDS.remove(bird)


def main():
    for x in range(50):
        bird = Bird(BIRD_START_X, BIRD_START_Y)
        BIRDS.append(bird)

    PIPES.append(Pipe(PIPE_START_GAP))
    PIPES.append(Pipe(PIPE_START_GAP + PIPE_GAP))

    base = Base(BASE_HEIGHT)
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_birds()
        handle_pipes()

        base.move()
        draw_window(window, base)
    pygame.quit()


main()
