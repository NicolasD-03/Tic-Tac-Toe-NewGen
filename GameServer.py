import sys
from libs.netcode.server import GameServer

if __name__ == "__main__":
    if len(sys.argv) == 2:
        server = GameServer(int(sys.argv[1]))
    else:
        server = GameServer(5556)

    server.start()
