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
        self.dots_group = pygame.sprite.Group()

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

        # Ajouter les points sur le terrain de jeu
        for i, row in enumerate(environment()):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j*32+12, i*32+12, WHITE, 8, 8))

        # Charge les effets sonores
        self.pacman_sound = pygame.mixer.Sound("pacman_sound.wav")
        self.game_over_sound = pygame.mixer.Sound("game_over_sound.wav")

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
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True
                return False
                
    def run_logic(self):
        if not self.game_over:
            self.player.update(self.horizontal_blocks, self.vertical_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)

            # Lorsque le block_hit_list contient un sprite, cela signifie que le joueur a touché un point
            if len(block_hit_list) > 0:
                # Déclenchement de l'effet sonore
                self.pacman_sound.play()
                self.score += 1

            block_hit_list = pygame.sprite.spritecollide(self.player, self.fantomes, True)
            if len(block_hit_list) > 0:
                self.player.explosion = True
                self.game_over_sound.play()
                self.game_over = self.player.game_over

            self.game_over = self.player.game_over
            self.fantomes.update(self.horizontal_blocks, self.vertical_blocks)
            # tkMessageBox.showinfo("GAME OVER !", "Score final = " + (str)(Game.score))
            messagebox.showinfo("GAME OVER !", "Score final = " + str(self.score))

    def display_frame(self, screen):
        # Tout d'abord, effacez l'écran. N'y mettez pas d'autres commandes de dessin
        screen.fill(BLACK)

        # ----- Le code pour dessiner le terrain de jeu vient ici -----
        if self.game_over:
            if self.about:
                self.display_message(screen, "C'est un jeu d'arcade")
                # "un labyrinthe contenant divers points,\n"
            else:
                self.menu.display_frame(screen)
        else:
            # ----- Dessin du terrain de jeu -----
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_environment(screen)
            self.dots_group.draw(screen)
            self.fantomes.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            #text = self.font.render("Score : " + str(self.score), True, RED)
            screen.blit(text, (30, 650))

            # Affiche le texte du score
            text = self.font.render("Score : " + str(self.score), True, GREEN)

            # Dessin le texte à l'écran
            screen.blit(text, [120, 20])

            # Met à jour l'écran
            pygame.display.flip()

    
    def display_message(self, screen, message, color=(255,0,0)):
        label = self.font.render(message, True, color)
        # Obtenir la largueur et la hauteur de l'étiquette
        width = label.get_width()
        height = label.get_height()

        # Détermine la position de l'étiquette sur l'écran
        posX = (SCREEN_WIDTH / 2) - (width / 2)
        posY = (SCREEN_HEIGHT / 2) - (height / 2)

        # Dessine l'étiquette sur l'écran
        screen.blit(label, (posX, posY))


class Menu(object):
    state = 0
    def __init__(self, items, font_color=(0,0,0), select_color=(255,0,0), ttf_font=None, font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font, font_size)

    def display_frame(self, screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item, True, self.select_color)
            else:
                label = self.font.render(item, True, self.font_color)
            width = label.get_width()
            height = label.get_height()
            posX = (SCREEN_WIDTH / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)
            screen.blit(label, (posX, posY))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) - 1:
                    self.state += 1

                    

