from typing import Any
import pygame
import random
from threading import Timer

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
# ----CONFIG----
# DONT CHANGE THE VALUES HERE! these are only for syntax highlighting
# ONLY CHANGE IN config.toml
STAR_COUNT_MIN: int = 0
STAR_COUNT_MAX: int = 0
STAR_BRIGHTNESS_MIN: int = 0
STAR_BRIGHTNESS_MAX: int = 0
STAR_SIZE_MIN: int = 0
STAR_SIZE_MAX: int = 0
PLAYER_SPAWN_X: int = 0
PLAYER_SPAWN_Y: int = 0
PLAYER_SPEED: int = 0
PLAYER_SPRINT: int = 0
ENEMY_SPAWN_X: int = 0  # DEPRECATED(see config)
ENEMY_SPAWN_Y: int = 0
ENEMY_SPEED: int = 0
ENEMY_COUNT_MIN: int = 0
ENEMY_COUNT_MAX: int = 0
BACKGROUND: tuple = (0, 0, 0)

with open("./config.toml", "rb") as f:
    data: dict[str, Any] = tomllib.load(f)
for d in data:
    globals()[d] = data.get(d)
# -------------
# background: pygame.image = pygame.image.load('bg.jpg')
pygame.init()
screen: pygame.display = pygame.display.set_mode()
clock: pygame.time = pygame.time.Clock()
dt: clock = None


class Player:
    def __init__(self) -> None:
        # self.pos = pygame.Vector2(100, 100)
        self.spaceship: pygame.image = pygame.image.load(
            './assets/img/player.png'
        )
        self.spaceShipRect: pygame.rect = self.spaceship.get_rect()
        # CALCULATE % VALUES
        spawnX: int = int(
            (screen.get_width() * (PLAYER_SPAWN_X / 100) - (self.spaceShipRect.width * (PLAYER_SPAWN_X / 100))))
        spawnY: int = int(
            (screen.get_height() * (PLAYER_SPAWN_X / 100) - (self.spaceShipRect.height * (PLAYER_SPAWN_X / 100))))
        self.spaceShipRect.update(spawnX, spawnY, self.spaceShipRect.height, self.spaceShipRect.width)

    def handle_pressed_keys(self) -> None:
        sprint: int = 0
        playerKeys = pygame.key.get_pressed()
        speed: int = PLAYER_SPEED

        if playerKeys[pygame.K_x]:
            sprint = PLAYER_SPRINT
        if (playerKeys[pygame.K_w] or playerKeys[pygame.K_UP]) and self.spaceShipRect.y > 0:
            self.spaceShipRect.y -= (speed + sprint) * dt
        if (playerKeys[pygame.K_s] or playerKeys[
            pygame.K_DOWN]) and self.spaceShipRect.y < screen.get_height() - self.spaceShipRect.height:
            self.spaceShipRect.y += (speed + sprint) * dt
        if (playerKeys[pygame.K_a] or playerKeys[pygame.K_LEFT]) and self.spaceShipRect.x > -10:
            self.spaceShipRect.x -= (speed + sprint) * dt
        if (playerKeys[pygame.K_d] or playerKeys[
            pygame.K_RIGHT]) and self.spaceShipRect.x < screen.get_width() - self.spaceShipRect.width:
            self.spaceShipRect.x += (speed + sprint) * dt


class Game:
    def __init__(self) -> None:
        self.player: Player = Player()
        self.isRunning: bool = True

    def loop(self) -> None:
        screen.fill(BACKGROUND)
        self.handlePlayer()

    def handlePlayer(self) -> None:
        self.player.handle_pressed_keys()
        screen.blit(self.player.spaceship, self.player.spaceShipRect)

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


frame: int = 0
game: Game = Game()

while game.isRunning:
    dt: clock = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.isRunning = False

    keys: pygame.key = pygame.key.get_pressed()
    game.loop()
    frame += 1
    pygame.display.flip()
game.quit()
