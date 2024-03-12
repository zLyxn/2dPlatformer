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
        screen.fill((230, 0, 230))

    def quit(self) -> None:
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
        self.body = pygame.transform.scale_by(self.body, (2, 2))
        self.bodyRect: pygame.Rect = self.body.get_rect()
        spawnX: int = int(
            (screen.get_width() * (PLAYER_SPAWN_X / 100) - (self.bodyRect.width * (PLAYER_SPAWN_X / 100))))
        spawnY: int = int(
            (screen.get_height() * (PLAYER_SPAWN_Y / 100) - (self.bodyRect.height * (PLAYER_SPAWN_Y / 100))))
        self.bodyRect.update(spawnX, spawnY, self.bodyRect.height, self.bodyRect.width)

        self.velocityY = 0

    def handleMovement(self):
        playerKeys = pygame.key.get_pressed()
        speed: int = PLAYER_SPEED
        if (playerKeys[pygame.K_w] or playerKeys[pygame.K_UP]) and self.bodyRect.y > 0:
            self.bodyRect.y -= 20
        if (playerKeys[pygame.K_a] or playerKeys[pygame.K_LEFT]) and self.bodyRect.x > -10:
            self.bodyRect.x -= speed * dt
        if (playerKeys[pygame.K_d] or playerKeys[
            pygame.K_RIGHT]) and self.bodyRect.x < screen.get_width() - self.bodyRect.width:
            self.bodyRect.x += speed * dt
        self.handleGravity()

    def handleGravity(self):
        speed: int = PLAYER_SPEED
        # Define gravity acceleration
        gravity = 100  # You can adjust this value to change the strength of gravity

        # Check if the player is not at the bottom of the screen
        if self.bodyRect.y < screen.get_height() - self.bodyRect.height:
            # Apply gravity acceleration to the vertical velocity
            self.velocityY += gravity * dt
            # Update the player's position based on vertical velocity
            self.bodyRect.y += self.velocityY * dt
        else:
            self.velocityY = 0


frame: int = 0
game: Game = Game()

while game.isRunning:
    dt: clock = clock.tick(120) / 1000
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

# IDEE FÜR GRÖßE
# var = screen.width/12,8
# block.height = var
# block.width = var
