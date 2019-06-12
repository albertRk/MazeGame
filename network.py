import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.43.77"
        self.port = 7777
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def send(self, data):
        try:
            print(data)
            self.client.send(str.encode(data))
        except socket.error as e:
            print(e)
        return self.client.recv(2048).decode()
    def sendWithoutRespond(self, data):
        try:
            print(data)
            self.client.send(str.encode(data))
        except socket.error as e:
            print(e)
    def connect(self):
        try:
            self.client.connect(self.addr)
        except:
            pass
