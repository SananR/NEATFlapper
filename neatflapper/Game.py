import pygame
from neatflapper.utils.game.Bird import Bird
from neatflapper.utils.game.Base import Base
from neatflapper.utils.game.Pipe import Pipe
from neatflapper.utils import Resources
import pythonneat.neat.Evolution as Evolution


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
        if not bird.alive:
            continue
        render_lines(bird, window)
        bird.draw(window)
    for pipe in PIPES:
        pipe.draw(window)

    base.draw(window)
    pygame.display.update()


def render_lines(bird, window):
    bird_mid = Resources.get_bird_mid(bird)
    pygame.draw.lines(window, (255, 0, 0), False, [bird_mid, Resources.get_pipe_top_mid(bird.next_pipe)], 3)
    pygame.draw.lines(window, (255, 0, 0), False, [bird_mid, Resources.get_pipe_bottom_mid(bird.next_pipe)], 3)


def handle_pipes():
    for pipe in PIPES:
        pipe.move()
        if pipe.x + Resources.PIPE_IMG.get_width() < 0:
            PIPES.remove(pipe)
        if not pipe.passed and pipe.x + Resources.PIPE_IMG.get_width() < BIRD_START_X:
            pipe.passed = True
            PIPES.append(Pipe(PIPES[len(PIPES) - 1].x + PIPE_GAP))
            for bird in BIRDS:
                if bird.alive:
                    bird.score += 1


def handle_birds():
    for bird in BIRDS:
        if not bird.alive:
            continue
        bird.act(PIPES)

        bird.move()
        if PIPES[0].collide(bird):
            bird.alive = False
        elif bird.y + bird.img.get_height() >= WIN_HEIGHT or bird.y + bird.img.get_height() <= 0:
            bird.alive = False


def population_dead():
    for bird in BIRDS:
        if bird.alive:
            return False
    return True


def evaluate_population(networks):
    BIRDS.clear()
    PIPES.clear()

    PIPES.append(Pipe(PIPE_START_GAP))
    PIPES.append(Pipe(PIPE_START_GAP + PIPE_GAP))

    for i in range(len(networks)):
        bird = Bird(BIRD_START_X, BIRD_START_Y, networks[i])
        bird.next_pipe = PIPES[0]
        BIRDS.append(bird)


def game_loop(networks):
    base = Base(BASE_HEIGHT)
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    evaluate_population(networks)
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if population_dead():
            fitness = []
            for i in range(len(BIRDS)):
                fitness.append(BIRDS[i].score)
            return fitness

        handle_pipes()
        handle_birds()

        base.move()
        draw_window(window, base)

    pygame.quit()


Evolution.start_evolution(6, 1, game_loop)


