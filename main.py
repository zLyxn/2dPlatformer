from typing import Any
import pygame

# from threading import Timer

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

PLAYER_SPEED: int = 0
PLAYER_SPAWN_X: int = 0
PLAYER_SPAWN_Y: int = 0

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
        self.player: Player = Player()

    def loop(self) -> None:
        self.handleBackground()
        self.handlePlayer()

    def handlePlayer(self) -> None:
        self.player.handleMovement()
        screen.blit(self.player.body, self.player.bodyRect)

    def handleBackground(self) -> None:
        bg: pygame.image = pygame.image.load("./assets/img/player.png")
        screen.blit(bg, (0, 0))

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
        self.body: pygame.image = pygame.image.load(
            './assets/img/player.png'
        )
        self.bodyRect: pygame.Rect = self.body.get_rect()
        spawnX: int = int(
            (screen.get_width() * (PLAYER_SPAWN_X / 100) - (self.bodyRect.width * (PLAYER_SPAWN_X / 100))))
        spawnY: int = int(
            (screen.get_height() * (PLAYER_SPAWN_Y / 100) - (self.bodyRect.height * (PLAYER_SPAWN_Y / 100))))
        self.bodyRect.update(spawnX, spawnY, self.bodyRect.height, self.bodyRect.width)

    def handleMovement(self) -> None:
        playerKeys = pygame.key.get_pressed()
        speed: int = PLAYER_SPEED

        if (playerKeys[pygame.K_w]) and self.bodyRect.y > 0:
            self.bodyRect.y -= speed * dt


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
