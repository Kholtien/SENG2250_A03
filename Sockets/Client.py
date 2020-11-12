import socket               # Import socket module
from otherFunctions import otherFunctions as oF
import random

class Client:
    def __init__(self):
        self.clientID = random.randrange(999999999)
        self.startClient()


    def connectToServer(self):
        s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12543                # Reserve a port for your service.

        s.connect((host, port))
        self.sendHello(s)
        return s

    def sendHello(self,socket):
        socket.send(b'Hello')

    def closeConnection(self,socket):
        socket.close()

    def killServer(self,socket):
        socket.send(b'closeServer')
    
    def receiveRsaPublicKey(self,socket):
        print('Receiveing Public Key from Server')
        message = socket.recv(4096)
        print('public Key: ',message)
    
    def startClient(self):
        s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12543                # Reserve a port for your service.

        s.connect((host, port))
        print(s.recv(4096))
        s.send(b'Hello')
        
        print('Receiveing Public Key from Server')
        RsaPublicKeyString = s.recv(4096).decode()
        RsaPublicKey = tuple(map(int, RsaPublicKeyString.replace('(','').replace(')','').split(', ')))
        print('public Key:\n',RsaPublicKey,'\n')

        
        print(self.clientID)
        encryptedClientID = oF.rsaEncrypt(self.clientID,int(RsaPublicKey[1]),int(RsaPublicKey[0]))
        print('now sending Client ID:',self.clientID,'as',encryptedClientID)
        s.send(('IDc: ' + str(encryptedClientID)).encode())
        print('Sent Client ID\n')

        #TODO receive ServerID part of handshake