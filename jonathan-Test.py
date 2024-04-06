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
PLAYER_JUMP = -15  # evtl -9
PLAYER_SPEED = 5

coinCollected = False

# Erstellung des Fensters
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("von Mika und Jonathan")

# Block definieren
BLOCK_SIZE = screen.get_width() / 16

# default Position
playerPosition = pygame.Vector2(5, 2)


class Game:
    def __init__(self):
        self.level = Level()
        self.player = Player(self.level)  # Übergebe eine Instanz des aktuellen Levels an den Spieler

    def game_loop(self):
        screen.fill(LIGHT_BLUE)
        self.level.draw()
        self.player.draw()
        pygame.display.flip()

        self.player.update()
        self.player_move()

    def player_move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and not self.player.is_block_above() and self.player.rect.top > 0:
            self.player.jump()  # Änderung: Spieler springen lassen, wenn W gedrückt wird
        if keys[pygame.K_a] and not self.player.is_block_left() and self.player.rect.left > 0:
            self.player.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d] and not self.player.is_block_right() and self.player.rect.right < screen.get_width():
            self.player.rect.x += PLAYER_SPEED


# Spieler-Klasse
class Player(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = pygame.image.load("./assets/img/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(BLOCK_SIZE / 2), int(BLOCK_SIZE)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (BLOCK_SIZE * playerPosition.x, BLOCK_SIZE * playerPosition.y)
        self.velocity_y = 0
        self.on_ground = False
        self.level = level

    def update(self):
        self.rect.y += self.velocity_y

        # Überprüfen, ob der Spieler auf dem Boden steht oder auf einem Block steht
        if self.rect.bottom >= screen.get_height() or self.is_block_below():
            if self.rect.bottom >= screen.get_height():
                self.rect.bottom = screen.get_height()
            self.on_ground = True
            self.velocity_y = 0
        else:
            self.velocity_y += PLAYER_GRAVITY

            # Wenn der Spieler nach unten fällt und auf einen Block trifft, passen Sie seine Position entsprechend an
            if self.velocity_y > 0:
                for block in self.level.blocks_group:
                    if block.rect.colliderect(self.rect):
                        if self.rect.bottom > block.rect.top and self.rect.top < block.rect.top:
                            # Spieler fällt von oben auf den Block
                            self.rect.bottom = block.rect.top
                            self.on_ground = True
                            self.velocity_y = 0
                        elif self.rect.top < block.rect.bottom and self.rect.bottom > block.rect.bottom:
                            # Spieler stößt von unten gegen den Block
                            self.rect.top = block.rect.bottom
                            self.velocity_y = 0
                        else:
                            # Standardkollision, seitlicher Zusammenstoß mit dem Block
                            if self.velocity_y > 0:
                                self.rect.bottom = block.rect.top
                                self.on_ground = True
                                self.velocity_y = 0
                            else:
                                self.rect.top = block.rect.bottom
                                self.velocity_y = 0
                        break

    def jump(self):
        if self.on_ground and not self.is_block_above():  # Nur wenn der Spieler auf dem Boden ist
            self.velocity_y = PLAYER_JUMP
            self.on_ground = False

    def draw(self):
        screen.blit(self.image, self.rect)

    def is_block_above(self):
        player_rect = self.rect
        for block in self.level.blocks_group:
            if block.rect.bottom == player_rect.top and player_rect.left < block.rect.right and player_rect.right > block.rect.left:
                return True
        return False

    def is_block_below(self):
        for block in self.level.blocks_group:
            if (block.rect.top == self.rect.bottom) and (block.rect.left <= self.rect.left) and (
                    block.rect.right >= self.rect.right):
                return True
        return False

    def is_block_left(self):
        player_rect = self.rect
        for block in self.level.blocks_group:
            if block.rect.right == player_rect.left and player_rect.top < block.rect.bottom and player_rect.bottom > block.rect.top:
                return True
        return False

    def is_block_right(self):
        player_rect = self.rect
        for block in self.level.blocks_group:
            if block.rect.left == player_rect.right and player_rect.top < block.rect.bottom and player_rect.bottom > block.rect.top:
                return True
        return False


class Level:
    def __init__(self):
        self.blocks_group = pygame.sprite.Group()
        self.create_blocks()

    def create_blocks(self):

        block_positions = [(x + 0, 1) for x in range(1, 17)]
        block_positions.extend([(x + 2, 3) for x in range(1, 5)])
        block_positions.extend([(x + 8, 2) for x in range(1, 3)])
        #block_positions.extend([(1, 1), (10, 2)])

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

    game.game_loop()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
