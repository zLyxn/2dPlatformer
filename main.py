from typing import Any
import pygame

# from threading import Timer

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

PLAYER_SPEED: int = 120
PLAYER_SPAWN_X: int = 50
PLAYER_SPAWN_Y: int = 50
GRAVITY: int = 100

# with open("./config.toml", "rb") as f:
#    data: dict[str, Any] = tomllib.load(f)
# for d in data:
#    globals()[d] = data.get(d)

pygame.init()
screen: pygame.display = pygame.display.set_mode()
clock: pygame.time.Clock = pygame.time.Clock()
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

    @staticmethod
    def handleBackground() -> None:
        bg: pygame.image = pygame.image.load("./assets/img/background.png")
        # screen.blit(bg, (0, 0))
        pygame.draw.rect(, "red", (100, 100))

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
        self.body = pygame.transform.scale_by(self.body, (0.3, 0.2))
        self.bodyRect: pygame.Rect = self.body.get_rect()
        spawnX: int = int(
            (screen.get_width() * (PLAYER_SPAWN_X / 100) - (self.bodyRect.width * (PLAYER_SPAWN_X / 100))))
        spawnY: int = int(
            (screen.get_height() * (PLAYER_SPAWN_Y / 100) - (self.bodyRect.height * (PLAYER_SPAWN_Y / 100))))
        self.bodyRect.update(spawnX, spawnY, self.bodyRect.height, self.bodyRect.width)

        self.velocityX = 0
        self.velocityY = 0

    def handleMovement(self) -> None:
        playerKeys = pygame.key.get_pressed()
        acceleration: float = 0.2  # Adjust acceleration for smoother movement
        max_speed: float = 5  # Adjust maximum speed
        self.handleGravity()

    def handleGravity(self) -> None:
        gravity: int = GRAVITY
        # self.bodyRect.y -= self.velocityY * dt
        # self.velocityY -= gravity
        if self.bodyRect.y < screen.get_height() - self.bodyRect.height:
            self.bodyRect.y += gravity * dt


frame: int = 0
game: Game = Game()

while game.isRunning:
    dt: clock = clock.tick(70) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.isRunning = False

    keys: pygame.key = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        game.isRunning = False

    game.loop()
    pygame.display.flip()
    # https://gamemaker.io/de/tutorials/easy-platformer
game.quit()
