# needed modules
import socket
import threading
import time
import random

# global variables defined
HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345
ADDR = (HOST, PORT)

BYTES = 1024
FORMAT = "utf-8"

EXIT = "EXIT"

# socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

users_list = []

room = True
allRooms = []

# inherited from inbuilt class threading.Thread
class Game(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        print("Object Created")
        self.turn = False
        self.player1 = conn
        self.player2 = None
        self.state = "RUN"

    def set_player2(self, conn):
        self.player2 = conn

    def isPlayer2_valid(self):
        return self.player2 != None

    def endGame(self, player):
        if player == "P1":
            self.player1.send(bytes("WIN", FORMAT))
            self.player2.send(bytes("LOST", FORMAT))
        else:
            self.player2.send(bytes("WIN", FORMAT))
            self.player1.send(bytes("LOST", FORMAT))

    # overriding run() method of threads
    def run(self):
        print(f"[ROOM STARTED]")
        # randomly selecting a player to start
        self.turn = random.choice([True, False])
        self.player1.send(bytes(str(self.turn), FORMAT))
        self.player2.send(bytes(str((not self.turn)), FORMAT))

        # state = "RUN"
        msg = ""
        while self.state == "RUN":
            time.sleep(0.01)
            if self.turn:
                msg = self.player1.recv(BYTES)
                if msg:
                    print(msg.decode())
                    if msg.decode().strip() == "BINGO":
                        self.endGame("P1")
                        self.state = "HALT"
                    self.player2.send(msg)
                    self.turn = False
            else:
                msg = self.player2.recv(BYTES)
                if msg:
                    print(msg.decode())
                    if msg.decode().strip() == "BINGO":
                        self.endGame("P2")
                        self.state = "HALT"
                    self.player1.send(msg)
                    self.turn = True


def start():
    global users_list, room
    server.listen(10)
    print(f"[LISTENING] server is listening on {HOST}")
    count = -1
    while True:
        time.sleep(0.01)
        conn, addr = server.accept()
        if room:
            g = Game(conn)
            room = False
            allRooms.append(g)
            print("[ROOM CREATED]")
            print('Player 1')
            count += 1
        else:
            if not allRooms[count].isPlayer2_valid():
                print('Player 2')
                allRooms[count].set_player2(conn)
                # starting thread, it automatically calls run() function
                allRooms[count].start()
            room = True
            print(f"[ROOMS]: {len(allRooms)}")

        print(f"[ACTIVE CONNECTIONS] {threading.active_count()}")


if __name__ == "__main__":
    print("[STARTING] server is starting ... ")
    start()
