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


class Game:
    def __init__(self):
        player = Player(1, 2)
        self.game_loop(player)

    def game_loop(self, player):
        screen.fill(LIGHT_BLUE)
        self.player_move(player)
        Level()

    def player_move(self, player):

        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_w]:
            print('Key pressed')
            player.rect.update(100, 100, BLOCK_SIZE, BLOCK_SIZE)


# Spieler-Klasse
class Player:
    def __init__(self, x, y):
        x -= 1
        self.image = pygame.image.load("./assets/img/player.png").convert_alpha()  # Bild laden
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE / 2, BLOCK_SIZE))  # Größe ändern
        self.rect = self.image.get_rect()  # Rect erstellen
        self.rect.update(BLOCK_SIZE * x, screen.get_height() - (BLOCK_SIZE * y), BLOCK_SIZE, BLOCK_SIZE)  # Position
        screen.blit(self.image, self.rect)

        self.on_ground = False  # Var ob der Spieler am Boden ist


class Block:
    def __init__(self, x, y):
        x -= 1
        self.image = pygame.image.load("./assets/img/grass.png")
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.image.get_rect()
        self.rect.update(BLOCK_SIZE * x, screen.get_height() - (BLOCK_SIZE * y), BLOCK_SIZE, BLOCK_SIZE)  # Position
        screen.blit(self.image, self.rect)


class Coin:
    def __init__(self, x, y):
        x -= 1
        self.image = pygame.image.load("./assets/img/coin.png")
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.image.get_rect()
        self.rect.update(BLOCK_SIZE * x, screen.get_height() - (BLOCK_SIZE * y), BLOCK_SIZE, BLOCK_SIZE)  # Position
        screen.blit(self.image, self.rect)


class Level:
    def __init__(self):
        self.one()

    def one(self):
        Block(1, 1)
        Block(2, 1)
        Block(3, 1)
        Block(4, 1)
        Block(5, 1)
        Block(6, 1)
        Block(7, 1)
        Block(8, 1)
        Block(9, 1)
        Block(10, 1)
        Block(11, 1)
        Block(12, 1)
        Block(13, 1)
        Block(14, 1)
        Block(15, 1)
        Block(16, 1)
        Player(1, 2)
        Coin(2, 2)


game = Game()
player = Player(1, 2)

# Game-Loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.game_loop(player)

    # FPS
    pygame.time.Clock().tick(60)

    # Macht zeichnen möglich
    pygame.display.flip()

pygame.quit()
sys.exit()
