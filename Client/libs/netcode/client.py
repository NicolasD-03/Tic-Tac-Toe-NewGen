import socket


class Client:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host: str, port: int) -> None:
        try:
            self.socket.connect((host, port))
        except ConnectionRefusedError:
            raise ConnectionRefusedError("Connection refused")

    def send(self, data: str) -> None:
        self.socket.send(data.encode())

    def receive(self) -> str:
        return self.socket.recv(1024).decode()


class ClientUDP:
    def __init__(self) -> str:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.socket.settimeout(10)

    def get_servers_list(self) -> str:
        print("Searching for servers...")
        self.socket.sendto(
            "SERVER_INFO_CLIENT".encode(), ("82.64.62.127", 5555)
        )
        try:
            msg = self.socket.recvfrom(1024)[0].decode()
            if len(msg) > 2:
                return msg.replace('"', "")[1:][:-1]
            else:
                return "NO_SERVERS"
        except socket.timeout:
            pass
