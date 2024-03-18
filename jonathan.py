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
pygame.display.set_caption("von Mika und Jonathan")

# Block definieren
BLOCK_SIZE = screen.get_width()/16

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
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./assets/img/grass.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))

        self.rect = self.image.get_rect()
        self.rect.x = BLOCK_SIZE * x
        self.rect.y = screen.get_height() - BLOCK_SIZE * y

# Erstellen der Spieler- und Plattformgruppen
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

player = Player()
all_sprites.add(player)



allPlatforms = [
    # - REIHE 1 -#
    Platform(0, 1),
    Platform(1, 1),
    Platform(2, 1),
    Platform(3, 1),
    Platform(4, 1),
    Platform(5, 1),
    Platform(6, 1),
    Platform(7, 1),
    Platform(8, 1),
    Platform(9, 1),
    Platform(10, 1),
    Platform(11, 1),
    Platform(12, 1),
    Platform(13, 1),
    Platform(14, 1),
    Platform(15, 1),
    # - REIHE 2 -#
    Platform(0, 1),
    Platform(1, 4),
    Platform(2, 4),
    Platform(3, 3)
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
