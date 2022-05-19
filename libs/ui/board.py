from tkinter import Frame, Label
from .button import BoardButton


class Board:
    def __init__(self, window, boardList) -> None:
        self.window = window
        self.board_list = boardList
        self.player = "X"
        self.main_window = Frame(self.window, bg="green")
        self.main_window.pack(fill="both", expand=True)
        self.board_window = Frame(self.main_window)
        self.board_window.pack()
        self.title = Label(self.main_window, text="Board", bg="green").pack()

        self.btn_1 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 0, "Y": 0},
            lambda: self.click(self.btn_1),
        )
        self.btn_2 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 1, "Y": 0},
            lambda: self.click(self.btn_2),
        )
        self.btn_3 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 2, "Y": 0},
            lambda: self.click(self.btn_3),
        )

        self.btn_4 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 0, "Y": 1},
            lambda: self.click(self.btn_4),
        )
        self.btn_5 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 1, "Y": 1},
            lambda: self.click(self.btn_5),
        )
        self.btn_6 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 2, "Y": 1},
            lambda: self.click(self.btn_6),
        )

        self.btn_7 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 0, "Y": 2},
            lambda: self.click(self.btn_7),
        )
        self.btn_8 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 1, "Y": 2},
            lambda: self.click(self.btn_8),
        )
        self.btn_9 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 2, "Y": 2},
            lambda: self.click(self.btn_9),
        )

    def click(self, btn) -> None:
        btn.change_text(self.player)
        self.board_list[btn.pos["X"]][btn.pos["Y"]] = self.player
        btn.disable()
        self.player = "O" if self.player == "X" else "X"
        self.check_winner()
        print(self.board_list)

    def check_winner(self) -> None:

        # Check rows
        for x in self.board_list:
            # Check rows
            if x[0] == x[1] == x[2] != "":
                print("Winner is: " + x[0])
                self.disable_all_buttons()
                return
        # Check coloumns
        if (
            self.board_list[0][0]
            == self.board_list[1][0]
            == self.board_list[2][0]
            != ""
        ):
            print("Winner is: " + self.board_list[0][0])
            self.disable_all_buttons()
            return
        elif (
            self.board_list[0][1]
            == self.board_list[1][1]
            == self.board_list[2][1]
            != ""
        ):
            print("Winner is: " + self.board_list[0][1])
            self.disable_all_buttons()
            return
        elif (
            self.board_list[0][2]
            == self.board_list[1][2]
            == self.board_list[2][2]
            != ""
        ):
            print("Winner is: " + self.board_list[0][2])
            self.disable_all_buttons()
            return

        # Check diagonals
        if (
            self.board_list[0][0]
            == self.board_list[1][1]
            == self.board_list[2][2]
            != ""
        ):
            print("Winner is: " + self.board_list[0][0])
            self.disable_all_buttons()
            return
        elif (
            self.board_list[0][2]
            == self.board_list[1][1]
            == self.board_list[2][0]
            != ""
        ):
            print("Winner is: " + self.board_list[0][2])
            self.disable_all_buttons()
            return

    def disable_all_buttons(self) -> None:
        self.btn_1.disable()
        self.btn_2.disable()
        self.btn_3.disable()
        self.btn_4.disable()
        self.btn_5.disable()
        self.btn_6.disable()
        self.btn_7.disable()
        self.btn_8.disable()
        self.btn_9.disable()
