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

# Pfad zu den Bildern
img_folder = os.path.join(os.getcwd(), "assets", "img")

# Erstellung des Fensters
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer")

# Spieler-Klasse
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(img_folder, "player.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.vel_y = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.vel_y = PLAYER_JUMP
        self.vel_y += PLAYER_GRAVITY
        self.rect.y += self.vel_y
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

# Plattform-Klasse
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(os.path.join(img_folder, "grass.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(self.image, (width, height))

# Erstellen der Spieler- und Plattformgruppen
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

BlockSize = screen.get_width()/16

allPlatforms = [
    Platform(0, HEIGHT - BlockSize, BlockSize, BlockSize),
    Platform(BlockSize, HEIGHT - BlockSize, BlockSize, BlockSize),
    Platform(BlockSize*2, HEIGHT - BlockSize, BlockSize, BlockSize),
    Platform(BlockSize*3, HEIGHT - BlockSize, BlockSize, BlockSize),
    Platform(BlockSize*4, HEIGHT - BlockSize, BlockSize, BlockSize),
    Platform(BlockSize*4, HEIGHT - BlockSize, BlockSize, BlockSize),
    Platform(BlockSize*6, HEIGHT - BlockSize, BlockSize, BlockSize),
    Platform(BlockSize*7, HEIGHT - BlockSize, BlockSize, BlockSize),
    Platform(BlockSize*8, HEIGHT - BlockSize, BlockSize, BlockSize),
    Platform(BlockSize*9, HEIGHT - BlockSize, BlockSize, BlockSize)
]


for platform in allPlatforms:
    platforms.add(platform)
    all_sprites.add(platform)

# Spiel-Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Kollisionen
    hits = pygame.sprite.spritecollide(player, platforms, False)
    if hits:
        player.rect.bottom = hits[0].rect.top
        player.vel_y = 0

    # Zeichnen
    screen.fill(LIGHT_BLUE)
    all_sprites.draw(screen)
    pygame.display.flip()

    # FPS
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
