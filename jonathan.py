import pygame
import sys
import os

# Initialisierung von Pygame
pygame.init()

# Fenstergröße
WIDTH = 800
HEIGHT = 600

# Farben
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)

# Spieler-Eigenschaften
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = -15
PLAYER_SPEED = 5

coinCollected = False

# Erstellung des Fensters
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("von Mika und Jonathan")

# Block definieren
BLOCK_SIZE = screen.get_width() / 16

# Spieler-Klasse
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./assets/img/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(BLOCK_SIZE / 2), int(BLOCK_SIZE)))
        self.rect = self.image.get_rect()

        self.rect.center = (BLOCK_SIZE * 1, screen.get_height() - BLOCK_SIZE * 1)
        self.vel_y = 0
        self.on_ground = False  # Hinzufügen einer Variablen, um zu überprüfen, ob der Spieler am Boden ist

    def update(self, coinCollected):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:  # Spieler kann nur springen, wenn er am Boden ist
            self.vel_y = PLAYER_JUMP
            self.on_ground = False  # Der Spieler hat den Boden verlassen, also ist er nicht mehr am Boden
        self.vel_y += PLAYER_GRAVITY
        self.rect.y += self.vel_y
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and (self.rect.right < screen.get_width() or coinCollected):
            self.rect.x += PLAYER_SPEED

    def check_collision(self, platforms):
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                # Überprüfen, ob der Spieler von oben auf die Plattform fällt
                if self.vel_y > 0 and self.rect.bottom > platform.rect.top and self.rect.top < platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                # Keine Kollisionserkennung, wenn der Spieler von unten gegen eine Plattform springt
                elif self.vel_y < 0 and self.rect.top < platform.rect.bottom and self.rect.bottom > platform.rect.bottom:
                    pass
                else:
                    # Standardkollision, wenn der Spieler seitlich gegen eine Plattform stößt
                    self.vel_y = 0
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        self.on_ground = True
                    else:
                        self.rect.top = platform.rect.bottom
                        self.on_ground = False

# Münzen-Klasse
class Coin:
    def __init__(self, x, y):
        self.image = pygame.image.load("./assets/img/coin.png")
        self.image = pygame.transform.scale(self.image, (int(BLOCK_SIZE), int(BLOCK_SIZE)))
        self.rect = self.image.get_rect()
        self.rect.x = BLOCK_SIZE * x
        self.rect.y = screen.get_height() - BLOCK_SIZE * y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def check_collision(self, coins, player, coinCollected):
        for coin in coins:
            if(coin.rect.colliderect(player.rect) or coinCollected):
                self.image = pygame.image.load("./assets/img/cloud.png")
                return True
            return False


# Plattform-Klasse
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, material):
        super().__init__()
        if material == 1:
            self.image = pygame.image.load("./assets/img/grass.png").convert_alpha()
        elif material == 2:
            self.image = pygame.image.load("./assets/img/dirt.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(BLOCK_SIZE), int(BLOCK_SIZE)))
        self.rect = self.image.get_rect()
        self.rect.x = BLOCK_SIZE * x
        self.rect.y = screen.get_height() - BLOCK_SIZE * y

class Game:
    def __init__(self):
        self.handle_end()
    def handle_end(self):
        if player.rect.x > screen.get_width():
            print("Game Over")
            screen.fill(LIGHT_BLUE)
            pygame.display.flip()
    def draw_level(self):
        if player.rect.x < screen.get_width():
            # Zeichnen
            screen.fill(LIGHT_BLUE)
            for platform in platforms:
                screen.blit(platform.image, platform.rect)
            for coin in coins:
                coin.draw(screen)
            screen.blit(player.image, player.rect)
            pygame.display.flip()

        return coin


# Erstellen der Plattformen
platforms = []
for row, platform_row in enumerate([
    [1] * 16,  # Reihe 1
    [0] * 8 + [1] * 2 + [0] * 6,  # Reihe 2
    [0] * 2 + [1] * 4 + [0] * 10,  # Reihe 3
]):
    for col, block in enumerate(platform_row):
        if block == 1:
            platforms.append(Platform(col, row + 1, 1))  # Beachte die Verschiebung um 1 für y, um Platz für den Spieler zu lassen
        elif block == 2:
            platforms.append(Platform(col, row + 1, 2))  # Beachte die Verschiebung um 1 für y, um Platz für den Spieler zu lassen

# Erstellen der Münzen
coins = [
    Coin(0, 6)
]

# Erstellen des Spielers
player = Player()
game = Game()

# Spiel-Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player.update(coinCollected)
    player.check_collision(platforms)  # Überprüfe die Kollisionen des Spielers

    coin = game.draw_level()

    coinCollected = coin.check_collision(coins, player, coinCollected)

    # FPS
    pygame.time.Clock().tick(60)

    # Spiel Ende
    game.handle_end()

pygame.quit()
sys.exit()
