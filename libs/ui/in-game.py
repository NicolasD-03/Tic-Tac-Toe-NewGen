from tkinter import Frame
from .button import MyButton
from .board import Board


class InGame:
    def __init__(self, window, boardList) -> None:
        self.window = Frame(window, height=900, width=900, bg="red")
        self.board = Board(
            self.window, [["", "", ""], ["", "", ""], ["", "", ""]]
        )

    def show(self) -> None:
        self.window.pack(fill="both", expand=True)
