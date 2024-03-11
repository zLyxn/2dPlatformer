from typing import Any
import pygame
from threading import Timer

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

with open("./config.toml", "rb") as f:
    data: dict[str, Any] = tomllib.load(f)
for d in data:
    globals()[d] = data.get(d)

pygame.init()
screen: pygame.display = pygame.display.set_mode()
clock: pygame.time = pygame.time.Clock()
dt: clock = None


class Game:
    def __init__(self) -> None:
        self.isRunning: bool = True

    def loop(self) -> None:
        pass

    @staticmethod
    def quit() -> None:
        pygame.quit()
        print("""
             ____             _ 
            | __ ) _   _  ___| |
            |  _ \| | | |/ _ \ |
            | |_) | |_| |  __/_|
            |____/ \__, |\___(_)
                   |___/        
        """)
        quit()


class Player:
    def __init__(self) -> None:
        pass


frame: int = 0
game: Game = Game()

while game.isRunning:
    dt: clock = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.isRunning = False

    keys: pygame.key = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        game.isRunning = False

    game.loop()
    # https://gamemaker.io/de/tutorials/easy-platformer
game.quit()
