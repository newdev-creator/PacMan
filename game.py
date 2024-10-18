import pygame
from player import Player
from fantomes import *
import tkinter
from tkinter import messagebox

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# Définit les couleurs du jeu
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Game(object):
    def __init__(self):
        self.font = pygame.font.Font(None, 40)
        self.about = False
        self.game_over = True

        # Crée la variable pour le score
        self.score = 0
        self.font = pygame.font.Font(None, 35)

        # Crée le menu du jeu
        self.menu = Menu(("Start", "A propos", "Exit"), font_color=WHITE, font_size=60)

        # Crée le personnage du joueur
        self.player = Player(32, 128, "player.png")

        # Crée les blocks qui définiront les chemins où le joueur peut aller
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()

        # Crée un groupe de points à l'écran
        self.dots = pygame.sprite.Group()

        # Définit l'environnement
        for i, row in enumerate(environment()):
            for j, item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j*32+8, i*32+8, BLACK, 16, 16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j*32+8, i*32+8, BLACK, 16, 16))

        # Création des fantomes
        self.fantomes = pygame.sprite.Group()
        self.fantomes.add(Fantome(288, 96, 0, 2))
        self.fantomes.add(Fantome(288, 320, 0, -2))
        self.fantomes.add(Fantome(544, 128, 0, 2))
        self.fantomes.add(Fantome(32, 224, 0, 2))
        self.fantomes.add(Fantome(160, 96, 2, 0))
        self.fantomes.add(Fantome(448, 64, -2, 0))
        self.fantomes.add(Fantome(640, 448, 2, 0))
        self.fantomes.add(Fantome(448, 320, 2, 0))

        # Ajouter les pointes sur le terrain de jeu
        for i, row in enumerate(environment()):
            if item != 0:
                self.dots_group.add(Ellipse(j*32+12, i*32+12, WHITE, 8, 8))

        # Charge les effets sonores
        self.pacman_sound = pygame.mixer.Sound("pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound("game_over_sound.ogg")

    def process_events(self):
        for event in pygame.event.get():
            # Détection des actions du joueur
            if event.type == pygame.QUIT:
                # Si le joueur a cliqué sur quitter proposer le choix entre START, A PROPOS et QUITTER
                return True
            
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about:
                        if self.menu.state == 0:
                            # ---- START -----
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 1:
                            # ----- A PROPOS -----
                            self.about = True
                        elif self.menu.state == 2:
                            # ----- QUITTER -----
                            return True
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_UP:
                    self.player.move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.move_down()
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.about = False
                elif event.type == pygame.KEYUP:
                    if event.type == pygame.K_RIGHT:
                        self.player.stop_move_right()
                    elif event.type == pygame.K_LEFT:
                        self.player.stop_move_left()
                    elif event.type == pygame.K_UP:
                        self.player.stop_move_up()
                    elif event.type == pygame.K_down:
                        self.player.stop_move_down()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.explosion = True
                    return False
                
    def run_logic(self):
        if not self.game_over:
            self.player.update(self.horizontal_blocks, self.vertical_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)

            # Lorsque le block_hit_list contient un sprite, cela signifie que le joueur a touché un point
            
                

