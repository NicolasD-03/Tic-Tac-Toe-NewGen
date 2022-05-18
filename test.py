from http import client
import socket


nickname = input("Enter your nickname: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 5556))
sock.send(nickname.encode())
