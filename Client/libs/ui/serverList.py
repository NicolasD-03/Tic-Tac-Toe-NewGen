from tkinter import Frame, Label, Entry
import sys
import ast

sys.path.append("../../../Tic-Tac-Toe-NewGen")

from libs.netcode.client import ClientUDP
from .button import MyButton, ConnectButton, DirectConnectButton


class ServerList:
    def __init__(self, root, client, joinMenu) -> None:
        self.root = root
        self.join_menu = joinMenu
        self.client = ClientUDP()
        self.server_list = []
        self.error_message = ""
        self.client_TCP = client
        self.main_window = Frame(self.root, bg="green")
        self.main_window.pack(fill="both", expand=True)
        self.server_list_window = Frame(self.main_window)
        self.server_list_window.pack()
        self.title = Label(
            self.main_window, text="Server List", bg="green"
        ).pack()
        self.refresh = MyButton(
            self.main_window,
            "Refresh",
            self.update_list,
            size={"HEIGHT": 2, "WIDTH": 8},
        )
        self.nickname_label = Label(self.main_window, text="Nickname:")
        self.nickname_label.pack()
        self.nickname = Entry(self.main_window)
        self.nickname.pack()
        self.ip_label = Label(self.main_window, text="IP:")
        self.ip_label.pack()
        self.ip_entry = Entry(self.main_window)
        self.ip_entry.pack()
        self.port_label = Label(self.main_window, text="Port:")
        self.port_label.pack()
        self.port_entry = Entry(self.main_window)
        self.port_entry.pack()
        self.direct_connect_btn = DirectConnectButton(
            self.main_window, self, size={"HEIGHT": 2, "WIDTH": 10}
        )

    def update_list(self) -> None:
        result = self.client.get_servers_list()
        self.server_list = []
        if result == "NO_SERVERS":
            self.error_message = "No servers found"
            self.server_list = []
        else:
            self.server_list = ast.literal_eval(result)
            self.error_message = ""
        self.update_interface()

    def update_interface(self) -> None:
        self.clear_frame()
        if self.error_message != "No servers found":
            if type(self.server_list) != dict:
                for i in range(len(self.server_list)):
                    Label(self.server_list_window, text=f"Server{i+1}").grid(
                        padx=10, row=i, column=0
                    )
                    Label(
                        self.server_list_window,
                        text=f"PORT:{self.server_list[i]['PORT']}",
                    ).grid(row=i, column=1)
                    Label(
                        self.server_list_window,
                        text=f"{len(self.server_list[i]['CLIENTS'])}/2",
                    ).grid(padx=10, pady=10, row=i, column=2)

                    ConnectButton(
                        self.server_list_window,
                        self,
                        self.server_list[i]["PORT"],
                        self.server_list[i]["CLIENTS"],
                        size={"HEIGHT": 2, "WIDTH": 8},
                        grid={"row": i, "column": 3},
                    )
            else:
                Label(self.server_list_window, text="Server").grid(
                    padx=10, row=0, column=0
                )
                Label(
                    self.server_list_window,
                    text=f"PORT:{self.server_list['PORT']}",
                ).grid(row=0, column=1)
                Label(
                    self.server_list_window,
                    text=f"{len(self.server_list['CLIENTS'])}/2",
                ).grid(padx=10, pady=10, row=0, column=2)
                ConnectButton(
                    self.server_list_window,
                    self,
                    self.server_list["PORT"],
                    self.server_list["CLIENTS"],
                    size={"HEIGHT": 2, "WIDTH": 8},
                    grid={"row": 0, "column": 3},
                )
        else:
            Label(self.server_list_window, text=self.error_message).pack()

    def clear_frame(self) -> None:
        for widget in self.server_list_window.winfo_children():
            widget.destroy()
