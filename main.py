import pygame
from game import Game

# Constantes de jeu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576
FPS = 30

def main():
    """
    Fonction principale du jeu Pac-Man.
    Initialise le jeu et gère la boucle principale.
    """
    try:
        # Initialisation de Pygame
        pygame.init()

        # Configuration de l'écran
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")

        # Initialisation du chronomètre
        clock = pygame.time.Clock()

        # Création de l'instance de jeu
        game = Game()

        # Boucle de jeu principale
        running = True
        while running:
            # Gestion des événements
            running = not game.process_events()  # Inverse la valeur car process_events retourne True pour quitter

            # Mise à jour de la logique du jeu
            game.run_logic()

            # Rendu de l'écran
            game.display_frame(screen)
            pygame.display.flip()  # Ajout de la mise à jour de l'affichage

            # Contrôle de la fréquence d'imagesa
            clock.tick(FPS)

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    
    finally:
        # Nettoyage et fermeture propre
        pygame.quit()

if __name__ == '__main__':
    main()