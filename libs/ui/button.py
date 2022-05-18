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


class BoardButton(MyButton):
    def __init__(self, window, title, size, pos, send_command="") -> None:
        self.send_command = send_command
        self.window = window
        self.my_btn = Button(
            window,
            text=title,
            command=self.click,
            height=size["HEIGHT"],
            width=size["WIDTH"],
        )
        self.pos = pos
        self.my_btn.grid(row=pos["X"], column=pos["Y"])

    def click(self) -> None:
        self.send_command(self.pos, "x")


class ConnectButton:
    def __init__(self, window, command, size, grid) -> None:
        self.my_btn = Button(
            window,
            text="Connect",
            command=command,
            height=size["HEIGHT"],
            width=size["WIDTH"],
        )
        self.window = window
        self.my_btn.grid(row=grid["row"], column=grid["column"])
