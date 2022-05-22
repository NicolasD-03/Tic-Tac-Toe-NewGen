from tkinter import Frame, Label, Button
import threading
import time


class BoardButton:
    def __init__(self, window, title, size, pos, command, id) -> None:
        self.window = window
        self.title = title
        self.size = size
        self.pos = pos
        self.command = command
        self.id = id
        self.my_btn = Button(
            self.window,
            text=self.title,
            command=self.command,
            height=self.size["HEIGHT"],
            width=self.size["WIDTH"],
        )
        self.my_btn.grid(row=pos["X"], column=pos["Y"])

    def change_text(self, text) -> None:
        self.my_btn.config(text=text)

    def disable(self) -> None:
        self.my_btn.config(state="disabled")


class Board:
    def __init__(self, player, client) -> None:
        self.client = client
        self.board_list = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.player = player
        self.message = ""
        self.label_message = ""
        self.your_turn = None
        self.main_window = Frame(None, bg="green")
        self.main_window.pack(fill="both", expand=True)
        self.board_window = Frame(self.main_window)
        self.board_window.pack()
        self.title = Label(self.main_window, text="Board", bg="green")
        self.player_info = Label(
            self.main_window, text=f"You are: {self.player}", bg="green"
        )
        self.label_info = Label(self.main_window, text="UwU", bg="green")

        self.btn_1 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 0, "Y": 0},
            lambda: self.click(self.btn_1),
            "btn_1",
        )
        self.btn_2 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 1, "Y": 0},
            lambda: self.click(self.btn_2),
            "btn_2",
        )
        self.btn_3 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 2, "Y": 0},
            lambda: self.click(self.btn_3),
            "btn_3",
        )

        self.btn_4 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 0, "Y": 1},
            lambda: self.click(self.btn_4),
            "btn_4",
        )
        self.btn_5 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 1, "Y": 1},
            lambda: self.click(self.btn_5),
            "btn_5",
        )
        self.btn_6 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 2, "Y": 1},
            lambda: self.click(self.btn_6),
            "btn_6",
        )

        self.btn_7 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 0, "Y": 2},
            lambda: self.click(self.btn_7),
            "btn_7",
        )
        self.btn_8 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 1, "Y": 2},
            lambda: self.click(self.btn_8),
            "btn_8",
        )
        self.btn_9 = BoardButton(
            self.board_window,
            "",
            {"HEIGHT": 2, "WIDTH": 8},
            {"X": 2, "Y": 2},
            lambda: self.click(self.btn_9),
            "btn_9",
        )

        self.title.pack()
        self.label_info.pack()

        self.receive_message_thread = threading.Thread(
            target=self.receive_message
        )
        self.receive_message_thread.start()

    def click(self, btn) -> None:
        if self.your_turn is True:
            print(btn.id)
            # time.sleep(0.5)
            self.client.send(f"CLICK>{btn.id}>{btn.pos}>{self.player}")

    def receive_message(self) -> None:
        while True:
            try:
                self.message = self.client.receive()

                if self.message.split(">")[0] == "TURN":
                    if self.message.split(">")[1] == self.player:
                        self.label_message = "Your turn"
                        self.your_turn = True
                    else:
                        self.label_message = "Opponent's turn"
                        self.your_turn = False
                    self.label_info.config(text=self.label_message)
                elif self.message.split(">")[0] == "MOVE":
                    btn = self.message.split(">")[1]
                    player = self.message.split(">")[2]
                    self.check_buttons(btn, player)
                elif self.message.split(">")[0] == "WINNER":
                    winner = self.message.split(">")[1]
                    self.label_message = f"{winner} won"
                    self.label_info.config(text=self.label_message)
                    self.disable_all_buttons()
                    break
                elif self.message.split(">")[0] == "DRAW":
                    self.label_message = "Draw"
                    self.label_info.config(text=self.label_message)
                    break
            except ConnectionResetError:
                break

    def check_buttons(self, btn, player):
        if btn == "btn_1":
            self.btn_1.change_text(player)
            self.board_list[0][0] = player
            self.btn_1.disable()
        elif btn == "btn_2":
            self.btn_2.change_text(player)
            self.board_list[0][1] = player
            self.btn_2.disable()
        elif btn == "btn_3":
            self.btn_3.change_text(player)
            self.board_list[0][2] = player
            self.btn_3.disable()
        elif btn == "btn_4":
            self.btn_4.change_text(player)
            self.board_list[1][0] = player
            self.btn_4.disable()
        elif btn == "btn_5":
            self.btn_5.change_text(player)
            self.board_list[1][1] = player
            self.btn_5.disable()
        elif btn == "btn_6":
            self.btn_6.change_text(player)
            self.board_list[1][2] = player
            self.btn_6.disable()
        elif btn == "btn_7":
            self.btn_7.change_text(player)
            self.board_list[2][0] = player
            self.btn_7.disable()
        elif btn == "btn_8":
            self.btn_8.change_text(player)
            self.board_list[2][1] = player
            self.btn_8.disable()
        elif btn == "btn_9":
            self.btn_9.change_text(player)
            self.board_list[2][2] = player
            self.btn_9.disable()

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
