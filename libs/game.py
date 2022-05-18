from tkinter import Tk
from libs.ui.menu import MainMenu, JoinMenu, GameMenu
from libs.netcode.client import Client


class Game:
    def __init__(self, settings) -> None:
        self.title = settings["TITLE"]
        self.width = settings["WIDTH"]
        self.height = settings["HEIGHT"]

        self.client = Client()

        self.root = Tk()
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}")

        self.main_menu = MainMenu(self)
        self.join_menu = JoinMenu(self, self.client)
        self.game_menu = GameMenu(self)

        self.main_menu.show()

    def show_join_menu(self) -> None:
        self.main_menu.unshow()
        self.join_menu.show()

    def show_main_menu(self) -> None:
        self.join_menu.unshow()
        self.game_menu.unshow()
        self.main_menu.show()

    def show_board(self) -> None:
        self.main_menu.unshow()
        self.game_menu.show()

    def quit(self) -> None:
        self.root.destroy()

    def start(self) -> None:
        self.root.mainloop()
