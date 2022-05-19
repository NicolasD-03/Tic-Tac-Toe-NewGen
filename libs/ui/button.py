from tkinter import Button


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


class BoardButton:
    def __init__(self, window, title, size, pos, command) -> None:
        self.window = window
        self.title = title
        self.size = size
        self.pos = pos
        self.command = command
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


class ConnectButton:
    def __init__(self, window, parent, port, size, grid) -> None:
        self.my_btn = Button(
            window,
            text="Connect",
            command=self.click,
            height=size["HEIGHT"],
            width=size["WIDTH"],
        )
        self.window = window
        self.my_btn.grid(row=grid["row"], column=grid["column"])
        self.parent = parent
        self.port = port

    def click(self) -> None:
        self.parent.client_TCP.connect("localhost", self.port)
        if self.parent.nickname.get() != "":
            self.parent.client_TCP.send(self.parent.nickname.get())
        else:
            self.parent.client_TCP.send("Anonymous")
