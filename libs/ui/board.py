from tkinter import Button, Frame
from .button import BoardButton


class Board:
    def __init__(self, window, boardList, update_list) -> None:
        self.update_list = update_list
        self.window = window
        self.board = Frame(self.window, height=600, width=600, bg="black")
        self.board.pack()
        for x in range(0, len(boardList)):
            for y in range(0, len(boardList[x])):
                BoardButton(
                    self.board,
                    boardList[x][y],
                    {"HEIGHT": 10, "WIDTH": 10},
                    {"X": x, "Y": y},
                    self.send,
                )

    def send(self, pos, player):
        self.update_list(pos, player)

    def update(self, boardList):
        self.board.destroy()
        self.board = Frame(self.window, height=600, width=600, bg="black")
        self.board.pack()
        for x in range(0, len(boardList)):
            for y in range(0, len(boardList[x])):
                BoardButton(
                    self.board,
                    boardList[x][y],
                    {"HEIGHT": 10, "WIDTH": 10},
                    {"X": x, "Y": y},
                )