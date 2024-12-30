# Entry point for the game
# Initialize Pygame and start the main game loop here

import pygame
from game.core.game_loop import Game

def main():
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
