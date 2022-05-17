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
