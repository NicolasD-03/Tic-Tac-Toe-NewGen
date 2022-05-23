import socket
import threading
import time
import ast


class MainServer:
    def __init__(self) -> None:
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_server.bind(("0.0.0.0", 5555))
        self.ports_range = range(5556, 5596)
        self.socket_server.settimeout(10)
        self.servers_list = []

    def get_servers_status(self) -> None:
        while True:
            time.sleep(1)
            self.servers_list = []
            for port in self.ports_range:
                self.socket_server.sendto(
                    "SERVER_INFO".encode(), ("192.168.2.2", port)
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