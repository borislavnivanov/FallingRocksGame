import random
import time
import pygame
from sys import exit
from multipledispatch import dispatch
from pygame import Surface, SurfaceType, Rect
from pygame.font import Font
from pygame.rect import RectType

COLORS: tuple = ('White', 'Green', 'Red')
CHAR_LIST = ['#', '*', '$', '&', '%']
WIDTH = 600
HEIGHT = 930
WEIGHTS: list = [7, 93]


class Object:
    def __init__(self, x, y):
        if x < 2:
            x = random_selector((10, screen.get_width() / 2))
        elif x > (WIDTH - 2):
            x = random_selector((screen.get_width() / 2, screen.get_width() - 10))
        self.position = [x, y]


class Dwarf(Object):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.show_char = '(@)'

    def __str__(self) -> Surface | SurfaceType:
        return font.render(f'{self.show_char}', True, 'White')

    def dwarf_move(self, direction):
        if direction == 'left':
            if self.position[0] > 5:
                self.position[0] -= 5
        elif direction == 'right':
            if self.position[0] < (screen.get_width() - 40):
                self.position[0] += 5


class Rock(Object):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.show_char = random.choice(CHAR_LIST)
        self.color = random_selector(COLORS)

    def __str__(self) -> Surface | SurfaceType:
        return font.render(f'{self.show_char}', True, self.color)

    def rock_move(self):
        self.position[1] += 5


@dispatch(list)
def random_selector(weights: list) -> bool:
    options: list = [True, False]
    result = random.choices(options, weights=weights, k=1)
    if result == [False]:
        return False
    else:
        return True


@dispatch(tuple)
def random_selector(selection: tuple) -> str:
    return random.choice(selection)


def collision_detection():
    global health
    health -= 1


def print_header(score: int):
    return font.render(f'Falling Rock score {score:05} | Health {health}', True, 'Green')


def background_builder() -> Surface | Rect | RectType:
    try:
        return pygame.image.load('pexels-philippe-donn-1257860.jpg').convert_alpha()
    except IOError:
        return pygame.Surface((WIDTH, HEIGHT)).fill('Black')


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Falling Rocks')
clock = pygame.time.Clock()
font: Font = pygame.font.Font(None, 30)
background = background_builder()
counter = pygame.Surface((screen.get_width(), 30))
counter.fill('Black')
player: Dwarf = Dwarf(screen.get_width() // 2, 900)

health: int = 5
rocks = []


def main():
    point_counter: int = 0

    while True:
        if health == 0:
            end_surface = font.render(f'GAME OVER', True, 'Blue', 'Red')
            game_over_background = pygame.Surface((WIDTH, HEIGHT))
            game_over_background.fill('Black')
            screen.blit(game_over_background, (0, 0))
            screen.blit(end_surface, (screen.get_width() / 2 - 100, screen.get_height() / 2))
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == pygame.K_LEFT:
                    player.dwarf_move('left')
                if event.key == pygame.K_RIGHT:
                    player.dwarf_move('right')
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        text_surface = print_header(point_counter)
        screen.blit(background, (0, 30))
        screen.blit(counter, (0, 0))
        screen.blit(text_surface, (10, 10))

        screen.blit(player.__str__(), player.position)

        if random_selector(WEIGHTS):
            rock: Rock = Rock(random.randrange(10, WIDTH - 20), 30)
            rocks.append(rock)

        for rock in rocks:
            screen.blit(rock.__str__(), rock.position)
        for rock in rocks:
            rock.rock_move()
            if rock.position[1] == player.position[1] and (
                    player.position[0] <= rock.position[0] <= (player.position[0] + 30)):
                collision_detection()
                rocks.clear()

            if rock.position[1] >= screen.get_height() - 15:
                point_counter += 1
                rocks.remove(rock)

        pygame.display.update()
        clock.tick(24)


if __name__ == '__main__':
    main()
