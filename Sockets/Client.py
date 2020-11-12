import socket               # Import socket module

class Client:
    def __init__(self):
        self.name = "client"


    def connectToServer(self):
        s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12345                # Reserve a port for your service.

        s.connect((host, port))
        print(s.recv(1024))
        return s

    def sendHello(self,socket):
        socket.send(b'Hello')

    def closeConnection(self,socket):
        socket.close()

    def killServer(self,socket):
        socket.send(b'closeServer')