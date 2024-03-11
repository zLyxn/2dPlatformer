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
        bg: pygame.image = pygame.image.load("./assets/img/background.png")
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
        self.body = pygame.transform.scale_by(self.body, (0.3, 0.2))
        self.bodyRect: pygame.Rect = self.body.get_rect()
        spawnX: int = int(
            (screen.get_width() * (PLAYER_SPAWN_X / 100) - (self.bodyRect.width * (PLAYER_SPAWN_X / 100))))
        spawnY: int = int(
            (screen.get_height() * (PLAYER_SPAWN_Y / 100) - (self.bodyRect.height * (PLAYER_SPAWN_Y / 100))))
        self.bodyRect.update(spawnX, spawnY, self.bodyRect.height, self.bodyRect.width)

        self.speed_x = 0

    def handleMovement(self) -> None:
        playerKeys = pygame.key.get_pressed()
        acceleration: float = 0.2  # Adjust acceleration for smoother movement
        max_speed: float = 5  # Adjust maximum speed
        gravity: float = 1.5

        # Horizontal Movement
        if playerKeys[pygame.K_a]:
            self.speed_x -= acceleration * dt
        elif playerKeys[pygame.K_d]:
            self.speed_x += acceleration * dt
        else:
            # Deceleration if no keys are pressed
            if self.speed_x > 0:
                self.speed_x -= acceleration * dt
            elif self.speed_x < 0:
                self.speed_x += acceleration * dt

        # Cap the speed
        self.speed_x = max(-max_speed, min(self.speed_x, int(max_speed)))

        # Update position
        self.bodyRect.x += self.speed_x

        # Vertical Movement (for jumping, etc.)
        if playerKeys[pygame.K_w] and self.bodyRect.y > 0:
            self.bodyRect.y -= PLAYER_SPEED * dt

        # Apply Gravity
        if self.bodyRect.y < screen.get_height() - self.bodyRect.height:
            self.bodyRect.y += gravity * dt

        # Limit Horizontal Speed
        if self.bodyRect.x < 0:
            self.bodyRect.x = 0
        elif self.bodyRect.x > screen.get_width() - self.bodyRect.width:
            self.bodyRect.x = screen.get_width() - self.bodyRect.width

        # Limit Vertical Speed
        if self.bodyRect.y < 0:
            self.bodyRect.y = 0
        elif self.bodyRect.y > screen.get_height() - self.bodyRect.height:
            self.bodyRect.y = screen.get_height() - self.bodyRect.height


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
    pygame.display.flip()
    # https://gamemaker.io/de/tutorials/easy-platformer
game.quit()
