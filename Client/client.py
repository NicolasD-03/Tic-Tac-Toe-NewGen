from telnetlib import GA
from libs.game import Game
from libs.load import settingsLoader

if __name__ == "__main__":
    settings = settingsLoader()
    game = Game(settings)
    game.start()
