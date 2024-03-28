import pygame
import sys

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

# default Position
playerPosition = pygame.Vector2(4, 2)


class Game:
    def __init__(self):
        self.player = Player()
        self.level = Level()

    def game_loop(self):
        screen.fill(LIGHT_BLUE)
        self.level.draw()
        self.player.draw()
        pygame.display.flip()

    def player_move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and not self.player.is_block_above(self.level.blocks_group) and self.player.rect.top > 0:
            self.player.jump()  # Änderung: Spieler springen lassen, wenn W gedrückt wird
        if keys[pygame.K_a] and not self.player.is_block_left(self.level.blocks_group) and self.player.rect.left > 0:
            self.player.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d] and not self.player.is_block_right(self.level.blocks_group) and self.player.rect.right < screen.get_width():
            self.player.rect.x += PLAYER_SPEED


# Spieler-Klasse
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./assets/img/player.png").convert_alpha()  # Bild laden
        self.image = pygame.transform.scale(self.image, (int(BLOCK_SIZE / 2), int(BLOCK_SIZE)))  # Größe ändern
        self.rect = self.image.get_rect()  # Rect erstellen
        self.rect.topleft = (BLOCK_SIZE * playerPosition.x, BLOCK_SIZE * playerPosition.y)  # Position
        self.velocity_y = 0  # Vertikale Geschwindigkeit des Spielers
        self.on_ground = False  # Variable zur Überprüfung, ob der Spieler auf dem Boden ist

    def update(self):
        # Bewegung aktualisieren
        self.rect.y += self.velocity_y

        # Spieler auf dem Boden halten
        if self.rect.bottom >= screen.get_height():
            self.rect.bottom = screen.get_height()
            self.on_ground = True
            self.velocity_y = 0
        else:
            self.velocity_y += PLAYER_GRAVITY  # Schwerkraft anwenden, um nach unten zu ziehen

    def jump(self):
        if self.on_ground:  # Nur wenn der Spieler auf dem Boden ist
            self.velocity_y = PLAYER_JUMP
            self.on_ground = False

    def draw(self):
        screen.blit(self.image, self.rect)

    def is_block_above(self, block_group):
        player_rect = self.rect
        for block in block_group:
            if block.rect.bottom == player_rect.top and player_rect.left < block.rect.right and player_rect.right > block.rect.left:
                return True
        return False

    def is_block_below(self, block_group):
        player_rect = self.rect
        for block in block_group:
            if block.rect.top == player_rect.bottom and player_rect.left < block.rect.right and player_rect.right > block.rect.left:
                return True
        return False

    def is_block_left(self, block_group):
        player_rect = self.rect
        for block in block_group:
            if block.rect.right == player_rect.left and player_rect.top < block.rect.bottom and player_rect.bottom > block.rect.top:
                return True
        return False

    def is_block_right(self, block_group):
        player_rect = self.rect
        for block in block_group:
            if block.rect.left == player_rect.right and player_rect.top < block.rect.bottom and player_rect.bottom > block.rect.top:
                return True
        return False


class Level:
    def __init__(self):
        self.blocks_group = pygame.sprite.Group()  # Erstelle eine Gruppe für die Blöcke
        self.create_blocks()  # Erstelle die Blöcke

    def create_blocks(self):
        # Erstelle die Blöcke und füge sie der Gruppe hinzu
        block_positions = [(x, 1) for x in range(1, 17)]  # Boden
        block_positions.extend([(5, 3), (10, 2)])  # Zusatz Blöcke
        for block_pos in block_positions:
            block = Block(*block_pos)
            self.blocks_group.add(block)

    def draw(self):
        self.blocks_group.draw(screen)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        x -= 1
        self.image = pygame.image.load("./assets/img/grass.png")
        self.image = pygame.transform.scale(self.image, (int(BLOCK_SIZE), int(BLOCK_SIZE)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (BLOCK_SIZE * x, screen.get_height() - (BLOCK_SIZE * y))  # Position


game = Game()

# Game-Loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.player_move()  # Spielerbewegung aktualisieren
    game.player.update()  # Spieler aktualisieren (z. B. für Schwerkraft)
    game.game_loop()  # Spiel-Loop aktualisieren

    # FPS
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
