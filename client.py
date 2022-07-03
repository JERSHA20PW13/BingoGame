import socket
import threading
import time

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345
ADDR = (HOST, PORT)

BYTES = 1024
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)


def receive():
    message = client.recv(BYTES)

    if len(message) != 0:
        return message.decode(FORMAT)

if __name__ == "__main__":
    while True:
        send(input())
