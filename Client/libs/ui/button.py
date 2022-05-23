from tkinter import Button

from .lobby import LobbyMenu


class MyButton:
    def __init__(self, window, title, command, size) -> None:
        self.my_btn = Button(
            window,
            text=title,
            command=command,
            height=size["HEIGHT"],
            width=size["WIDTH"],
        )
        self.my_btn.pack()


class ConnectButton:
    def __init__(self, window, parent, port, clients, size, grid) -> None:
        self.window = window
        self.parent = parent
        self.port = port
        self.clients = clients
        self.my_btn = Button(
            window,
            text="Connect",
            command=self.click,
            height=size["HEIGHT"],
            width=size["WIDTH"],
        )
        self.my_btn.grid(row=grid["row"], column=grid["column"])

        if len(self.clients) == 2:
            self.my_btn.config(state="disabled")

    def click(self) -> None:
        self.parent.client_TCP.connect("82.64.62.127", self.port)
        if self.parent.nickname.get() != "":
            self.parent.client_TCP.send(self.parent.nickname.get())
        else:
            self.parent.client_TCP.send("Anonymous")
        self.lobby_menu = LobbyMenu(self.parent.client_TCP)
        self.lobby_menu.show()
        self.parent.join_menu.unshow()


class DirectConnectButton:
    def __init__(self, window, parent, size) -> None:
        self.window = window
        self.parent = parent
        self.size = size
        self.my_btn = Button(
            self.window,
            text="Direct Connect",
            command=self.click,
            height=self.size["HEIGHT"],
            width=self.size["WIDTH"],
        )
        self.my_btn.pack()

    def click(self) -> None:
        if (
            self.parent.port_entry.get() != ""
            and self.parent.ip_entry.get() != ""
        ):
            self.parent.client_TCP.connect(
                self.parent.ip.get(), self.parent.port.get()
            )
            if self.parent.nickname.get() != "":
                self.parent.client_TCP.send(self.parent.nickname.get())
            else:
                self.parent.client_TCP.send("Anonymous")
            self.lobby_menu = LobbyMenu(self.parent.client_TCP)
            self.lobby_menu.show()
            self.parent.join_menu.unshow()
