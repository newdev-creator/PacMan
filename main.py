import pygame
from game import Game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

def main():
    # Initialisation de tous les modules pygame importés
    pygame.init()

    #Définit la largeur et la hauteur de l'écran [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Définit le titre de la fenêtre du jeu
    pygame.display.set_caption("Pac-Man")

    # Boucle jusqu'à ce que le joueur clique sur le bouton de fermeture
    done = False

    # Utilisé pour gérer la vitesse de mise à jour de l'écran
    clock = pygame.time.Clock()

    # Crée un élément du jeu
    game = Game()

    # ----- Boucle de jeu principale -----
    while not done:
        # ----- Traite les événements (frappes au clavier, clics de souris, etc.) -----
        done = game.process_events()

        # ----- la logique du jeu vient ici -----
        game.run_logic()

        # ----- Déssine l'écran du jeu -----
        game.display_frame(screen)

        # ----- Limite la vitesse d'affichage à 30 images par seconde -----
        clock.tick(30)
        # tkMessageBox.showinfo("GAME OVER !", "Score final = " + (str)(Game.score))

        # Ferme la fenêtre et quitter
        # Si vous oubliez cettte ligne, le programme se bloquera
        # à la sortie si vous exécutez le programme à partir de IDLE
        pygame.quit()

if __name__ == '__main__':
    main()