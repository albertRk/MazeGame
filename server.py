import socket
import threading
from _thread import *
import pygame
from game import Game


server = ''
port = 7777

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)

print("Waiting for a connection, Server Started")





def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def move(data, player):
    if data == (0, 1):
        theGame.players[player][1] = theGame.players[player][1] + 2 * theGame.speed
        if theGame.blocked(theGame.maze.maze, player):
            theGame.players[player][1] = theGame.players[player][1] - 2 * theGame.speed
    if data == (0, -1):
        theGame.players[player][1] = theGame.players[player][1] - 2 * theGame.speed
        if theGame.blocked(theGame.maze.maze, player):
            theGame.players[player][1] = theGame.players[player][1] + 2 * theGame.speed
    if data == (1, 0):
        theGame.players[player][0] = theGame.players[player][0] + 2 * theGame.speed
        if theGame.blocked(theGame.maze.maze, player):
            theGame.players[player][0] = theGame.players[player][0] - 2 * theGame.speed
    if data == (-1, 0):
        theGame.players[player][0] = theGame.players[player][0] - 2 * theGame.speed
        if theGame.blocked(theGame.maze.maze, player):
            theGame.players[player][0] = theGame.players[player][0] + 2 * theGame.speed


def threaded_client(conn):

    nick = conn.recv(2048).decode()
    i = 1
    while nick in theGame.players.keys():
        nick += str(i)
    color = conn.recv(2048).decode()
    theGame.players[nick] = [theGame.get_initpos()[0], theGame.get_initpos()[1], color, 0]
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())

            move(data, nick)
            if not data:
                print("Disconnected")

                break
        except:
            break
    del theGame.players[nick]
    print("Lost connection")
    conn.close()


def runGame():
    theGame.maze.generate_maze()

    theGame.on_init()
    theGame.name = ''
    while True:
        pygame.event.pump()
        theGame.on_render()


if __name__ == "__main__":
    theGame = Game()
    thread = threading.Thread(target=runGame)
    thread.start()
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        start_new_thread(threaded_client, (conn,))
