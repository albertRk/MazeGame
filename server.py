import socket
import threading
from _thread import *
import pygame
from game import Game

# ustawiamy tak server, żeby przyjmował wszystko i port dowolny
server = ''
port = 7777
# utworzenie i zbidnowanie socketu, a następnie nasłuchiwanie
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)

print("Waiting for a connection, Server Started")


# czytamy sobie wiadomosc rodzielajac string wspolrzednych na pojedyncze wspolrzedne
def read_pos(str):
    print(str)
    str = str.split(",")
    return int(str[0]), int(str[1])


# funkcja ktora odpowiada za ruch kropki
def move(data, player):
    if data == (0, 1):
        theGame.players[player][1] = theGame.players[player][1] + 2 * theGame.speed
        if theGame.blocked(theGame.maze.maze, theGame.players[player][0], theGame.players[player][1]):
            theGame.players[player][1] = theGame.players[player][1] - 2 * theGame.speed
    if data == (0, -1):
        theGame.players[player][1] = theGame.players[player][1] - 2 * theGame.speed
        if theGame.blocked(theGame.maze.maze, theGame.players[player][0], theGame.players[player][1]):
            theGame.players[player][1] = theGame.players[player][1] + 2 * theGame.speed
    if data == (1, 0):
        theGame.players[player][0] = theGame.players[player][0] + 2 * theGame.speed
        if theGame.blocked(theGame.maze.maze, theGame.players[player][0], theGame.players[player][1]):
            theGame.players[player][0] = theGame.players[player][0] - 2 * theGame.speed
    if data == (-1, 0):
        theGame.players[player][0] = theGame.players[player][0] - 2 * theGame.speed
        if theGame.blocked(theGame.maze.maze, theGame.players[player][0], theGame.players[player][1]):
            theGame.players[player][0] = theGame.players[player][0] + 2 * theGame.speed


# wątek odpowiedzialny za obsługe klienta tworzymy jeden dla każdego klienta
def threaded_client(conn):
    nick = conn.recv(2048).decode()
    i = 1
    # tutaj zapobiegamy powtórzeniu nicków poprzez dodanie liczby do nicku
    while nick in theGame.players.keys():
        nick += str(i)
    #  generujemy kolor
    color = theGame.colorGenerator()
    print(color)
    x, y = theGame.get_initpos()
    # ustawiamy podstawowe atrybuty graczy, które przechowujemy w słowniku
    theGame.players[nick] = [x, y, color, theGame.getStartPoints()]
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            if data[0] == 0 and data[1] == 0:
                break
            move(data, nick)
            # tutaj odsłyłamy cokolwiek, ponieważ bez tego odsyłania przychodziło wiecęj wiadomosci niż program czytał
            # i nagle musiał przeczytać za dużo, przy używaniu sleepa wystepowały laggi
            conn.send(str.encode("2"))
            if not data:
                print("Disconnected")
                break
        except:
            break
    del theGame.players[nick]
    print("Lost connection")
    conn.close()


# wątek odpowiedzialny za samą gre
def runGame():
    theGame.maze.generate_maze()

    theGame.on_init()
    theGame.name = ''
    while True:
        pygame.event.pump()
        theGame.on_render()


# w mainie przyjmujemy wiadomość i tworzymy wątek dla każdego klienta


if __name__ == "__main__":
    theGame = Game()
    thread = threading.Thread(target=runGame)
    thread.start()
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)
        start_new_thread(threaded_client, (conn,))
