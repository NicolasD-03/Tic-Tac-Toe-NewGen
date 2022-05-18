from http import server
import socket
import threading
import time

from libs.ui.serverList import ServerList


class MainServer:
    def __init__(self) -> None:
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_server.bind(("", 5555))
        self.ports_range = range(5556, 5576)
        self.socket_server.settimeout(1)
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
        self.socket_server.bind(("", self.port))
        self.socket_client.bind(("", self.port))
        self.socket_client.listen(5)

        self.game_status = "lobby"
        self.clients = []
        self.nicknames = []

    def broadcast(self, message: str) -> None:
        for client in self.clients:
            client.send(message.encode())

    def handle(self, client: socket.socket):
        while True:
            try:
                message = client.recv(1024)
                self.client_message_checks(message)
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

                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()
            else:
                break

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

    def client_message_checks(self, message) -> None:
        pass

    def start(self) -> None:
        print("Server started")
        threading.Thread(target=self.send_servers_status).start()
        self.waiting_connection()
