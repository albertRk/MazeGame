import json
import pickle
import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.8.197"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getMaze(self):
        try:
            return  json.loads(self.client.recv(56233).decode())
        except socket.error as e:
            print(e)

    def getPlayerNumber(self):
        return self.pos

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            data = json.loads(self.client.recv(2048).decode())
            return data
        except socket.error as e:
            print(e)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
