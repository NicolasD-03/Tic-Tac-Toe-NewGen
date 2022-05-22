from .button import MyButton
from .serverList import ServerList
from tkinter import Frame


class MainMenu:
    def __init__(self, window) -> None:
        self.main_menu = Frame(window.root, bg="yellow")
        self.join_btn = MyButton(
            self.main_menu,
            "Join",
            command=window.show_join_menu,
            size={"HEIGHT": 2, "WIDTH": 8},
        )
        self.quit_btn = MyButton(
            self.main_menu,
            "Quit",
            command=window.quit,
            size={"HEIGHT": 2, "WIDTH": 8},
        )

    def show(self) -> None:
        self.main_menu.pack(fill="both", expand=True)

    def unshow(self) -> None:
        self.main_menu.pack_forget()


class JoinMenu:
    def __init__(self, window, client) -> None:
        self.client = client
        self.root_window = window
        self.join_menu = Frame(window.root, bg="red")
        self.server_list = ServerList(self.join_menu, self.client, self)
        self.back_btn = MyButton(
            self.join_menu,
            "Back",
            command=window.show_main_menu,
            size={"HEIGHT": 2, "WIDTH": 8},
        )

    def show(self) -> None:
        self.join_menu.pack(fill="both", expand=True)

    def unshow(self) -> None:
        self.join_menu.pack_forget()


class GameMenu:
    def __init__(self, window) -> None:
        self.game_menu = Frame(window.root, bg="green")
        self.board_list = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.board = Board(self.game_menu, self.board_list, self.update_list)
        self.back_btn = MyButton(
            self.game_menu,
            "Back",
            command=window.show_main_menu,
            size={"HEIGHT": 2, "WIDTH": 8},
        )

    def update_list(self, pos, player) -> None:
        self.board_list[pos["X"]][pos["Y"]] = player
        self.board.update(self.board_list)
        print(self.board_list)

    def show(self) -> None:
        self.game_menu.pack(fill="both", expand=True)

    def unshow(self) -> None:
        self.game_menu.pack_forget()
