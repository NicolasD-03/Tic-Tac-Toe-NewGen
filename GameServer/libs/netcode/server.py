import socket
import threading
import time
import ast


class MainServer:
    def __init__(self) -> None:
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_server.bind(("0.0.0.0", 5555))
        self.ports_range = range(5556, 5576)
        self.socket_server.settimeout(10)
        self.servers_list = []

    def get_servers_status(self) -> None:
        while True:
            time.sleep(1)
            self.servers_list = []
            for port in self.ports_range:
                self.socket_server.sendto(
                    "SERVER_INFO".encode(), ("localhost", port)
                )

    def wait_reception(self) -> None:
        while True:
            try:
                addr = self.socket_server.recvfrom(1024)
                message = addr[0].decode()
                address = addr[1]
                if message == "SERVER_INFO_CLIENT":
                    self.send_servers_status(address)
                    print(message)
                elif message.split(">")[0] == "GAME_SERV":
                    self.servers_list.append(message.split(">")[1])
            except socket.timeout:
                pass

    def send_servers_status(self, address) -> None:
        server_list = str(self.servers_list).encode()

        self.socket_client.sendto(server_list, address)

    def start(self) -> None:
        threading.Thread(target=self.wait_reception).start()
        threading.Thread(target=self.get_servers_status).start()
        print("Server started")


class GameServer:
    def __init__(self, port: int) -> None:
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind(("0.0.0.0", self.port))
        self.socket_client.bind(("0.0.0.0", self.port))
        self.socket_client.listen(5)

        self.game_status = "lobby"
        self.clients = []
        self.nicknames = []
        self.player_turn = "X"
        self.turn = 0
        self.board_list = [["", "", ""], ["", "", ""], ["", "", ""]]

    def broadcast(self, message: str) -> None:
        for client in self.clients:
            client.send(message.encode())

    def handle(self, client: socket.socket):
        while True:
            try:
                message = client.recv(1024).decode()
                self.client_message_checks(message, client)
            except ConnectionResetError:
                break

    def waiting_connection(self) -> None:
        while True:
            if self.game_status == "lobby" and len(self.clients) < 2:
                client, address = self.socket_client.accept()
                nickname = client.recv(1024).decode()

                self.nicknames.append(nickname)
                self.clients.append(client)

                print(f"{nickname} connected")

                if len(self.clients) == 1:
                    player = "X"
                elif len(self.clients) == 2:
                    player = "O"

                client.send(f"PLAYER>{player}".encode())
                time.sleep(1)
                self.broadcast(f"LOBBY_INFO>{str(self.nicknames)}")

                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()

            else:
                pass

    def send_servers_status(self) -> None:
        while True:
            addr = self.socket_server.recvfrom(1024)
            message = addr[0].decode()
            address = addr[1]
            info_mess = str(
                {
                    "PORT": self.port,
                    "STATUS": self.game_status,
                    "CLIENTS": self.nicknames,
                }
            )
            if message == "SERVER_INFO":
                self.socket_server.sendto(
                    f"GAME_SERV>{info_mess}".encode(), address
                )

    def client_message_checks(self, message, client) -> None:
        if message.split(">")[0] == "START_GAME":
            self.game_status = "game"
            self.broadcast("GAME_STARTED")
            time.sleep(0.5)
            self.broadcast(f"TURN>{self.player_turn}")
        if message.split(">")[0] == "CLICK":
            btn_id = message.split(">")[1]
            btn_pos = ast.literal_eval(message.split(">")[2])
            player = message.split(">")[3]
            self.board_list[btn_pos["X"]][btn_pos["Y"]] = player
            self.turn += 1

            time.sleep(0.5)

            self.broadcast(f"MOVE>{btn_id}>{player}")

            time.sleep(0.5)

            winner = self.check_winner()

            if winner:
                self.broadcast(f"WINNER>{winner}")
                self.game_status = "lobby"
                self.clients = []
                self.nicknames = []
                self.board_list = [["", "", ""], ["", "", ""], ["", "", ""]]
            elif self.turn == 9:
                self.broadcast("DRAW")
                self.game_status = "lobby"
                self.clients = []
                self.nicknames = []
                self.board_list = [["", "", ""], ["", "", ""], ["", "", ""]]
            else:
                self.player_turn = "X" if self.player_turn == "O" else "O"
                self.broadcast(f"TURN>{self.player_turn}")

            print(self.board_list)

    def check_winner(self) -> None:
        # Check rows
        for x in self.board_list:
            # Check rows
            if x[0] == x[1] == x[2] != "":
                print("Winner is: " + x[0])
                return x[0]

        # Check coloumns
        if (
            self.board_list[0][0]
            == self.board_list[1][0]
            == self.board_list[2][0]
            != ""
        ):
            print("Winner is: " + self.board_list[0][0])
            return self.board_list[0][0]
        elif (
            self.board_list[0][1]
            == self.board_list[1][1]
            == self.board_list[2][1]
            != ""
        ):
            print("Winner is: " + self.board_list[0][1])
            return self.board_list[0][1]
        elif (
            self.board_list[0][2]
            == self.board_list[1][2]
            == self.board_list[2][2]
            != ""
        ):
            print("Winner is: " + self.board_list[0][2])
            return self.board_list[0][2]

        # Check diagonals
        if (
            self.board_list[0][0]
            == self.board_list[1][1]
            == self.board_list[2][2]
            != ""
        ):
            print("Winner is: " + self.board_list[0][0])
            return self.board_list[0][0]
        elif (
            self.board_list[0][2]
            == self.board_list[1][1]
            == self.board_list[2][0]
            != ""
        ):
            print("Winner is: " + self.board_list[0][2])
            return self.board_list[0][2]

    def start(self) -> None:
        print("Server started")
        threading.Thread(target=self.send_servers_status).start()
        self.waiting_connection()
