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


