from tkinter import Frame, Label, Button
import threading

from .board import Board


class LobbyMenu:
    def __init__(self, client) -> None:
        self.client = client
        self.message = ""
        self.player = ""
        self.clients = []
        self.lobby = Frame(None, bg="blue")

        self.receive_message_thread = threading.Thread(
            target=self.receive_message
        )
        self.receive_message_thread.start()

    def show(self) -> None:
        self.lobby.pack(fill="both", expand=True)

    def unshow(self) -> None:
        self.lobby.pack_forget()

    def receive_message(self):
        while True:
            try:
                self.message = self.client.receive()

                if self.message.split(">")[0] == "PLAYER":
                    self.player = self.message.split(">")[1]
                    print(self.player)
                elif self.message.split(">")[0] == "LOBBY_INFO":
                    self.clients = (
                        self.message.split(">")[1]
                        .replace("'", "")[1:][:-1]
                        .split(",")
                    )
                    self.update_interface()

                elif self.message.split(">")[0] == "GAME_STARTED":
                    self.unshow()
                    Board(self.player, self.client)
                    break
            except ConnectionResetError:
                break

    def update_interface(self):
        self.clear_frame()
        if len(self.clients) == 0:
            return
        for client in self.clients:
            Label(self.lobby, text=client, bg="blue").pack()

        self.start_btn = Button(
            self.lobby,
            text="Start",
            command=self.start_game,
            height=2,
            width=10,
        ).pack()

    def start_game(self):
        if len(self.clients) == 2:
            self.client.send("START_GAME")

    def clear_frame(self):
        for widget in self.lobby.winfo_children():
            widget.destroy()
