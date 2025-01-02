# Entry point for the game

from game.core.game_loop import Game

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
