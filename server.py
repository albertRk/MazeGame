import json
import pickle
import socket
from _thread import *
from maze import Maze
import sys

server = "10.129.13.79"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), str[2]


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def convert_maze(maze):
    result = dict()
    for c, key in enumerate(maze.maze.keys()):
        result[c] = maze.maze[key]
    return result

players = dict()


def threaded_client(conn, player):
    conn.sendall(str.encode(json.dumps(player)))
    conn.sendall(str.encode(json.dumps(maze.maze)))

    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            players[player] = data

            # print(players)
            print(data)
            if not data:
                print("Disconnected")
                break
            reply = players
            # print("Received: ", data)
            # print("Sending : ", reply)

            conn.sendall(str.encode(json.dumps(reply)))
        except:
            break

    print("Lost connection")
    conn.close()
if __name__ == "__main__":
    maze = Maze()
    maze.generate_maze()
    maze.convert_to_send()
    currentPlayer = 0
    while True:

        conn, addr = s.accept()
        print("Connected to:", addr)


        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1