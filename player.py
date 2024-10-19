import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# Définit certaines couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    explosion = False
    game_over = False

    def __init__(self, x, y, file_name):
        # Appelle le constructeur de la classe parent (sprite)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(file_name).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Charge l'image de l'animation
        img = pygame.image.load("walk.png").convert()

        # Crée les objets pour les animations
        self.move_right_animation = Animation(img, 32, 32)
        self.move_left_animation = Animation(pygame.transform.flip(img, True, False), 32, 32)
        self.move_up_animation = Animation(pygame.transform.rotate(img, 90), 32, 32)
        self.move_down_animation = Animation(pygame.transform.rotate(img, 270), 32, 32)

        # Charge l'image de l'explosion
        img = pygame.image.load("explosion.png").convert()
        self.explosion_animation = Animation(img, 32, 32)

        # Save the player image
        self.player_image = pygame.image.load(file_name).convert()
        self.player_image.set_colorkey(BLACK)

    def update(self, horizontal_blocks, vertical_blocks):
        
