import socket               # Import socket module
from otherFunctions import otherFunctions as oF
import random
import hashlib
from diffieHellman import diffieHellman as dh
from RSA_A03 import rsa

class Client:
    def __init__(self):
        self.clientID = random.randrange(999999999)
        self.diffieHellman = dh.DiffieHellman()
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
        RsaPublicKey = rsa.rsaBytesToTuple(s.recv(4096))
        # RsaPublicKeyString = s.recv(4096).decode()
        # RsaPublicKey = tuple(map(int, RsaPublicKeyString.replace('(','').replace(')','').split(', ')))
        print('public Key:\n',RsaPublicKey,'\n')

        
        print(self.clientID)

        encryptedClientID = rsa.rsaEncrypt(self.clientID,int(RsaPublicKey[1]),int(RsaPublicKey[0]))
        print('now sending Client ID:',self.clientID,'as',encryptedClientID)
        s.send(('IDc: ' + str(encryptedClientID)).encode())
        print('Sent Client ID\n')


        print('\nRecieving Server_Hello')
        Server_Hello = rsa.rsaBytesToTuple(s.recv(4096))
        serverAndSID = rsa.verifySignatureTuple(Server_Hello,RsaPublicKey)
        print('received Server_Hello as:',serverAndSID)
        serverID = serverAndSID[0]
        SID = serverAndSID[1]
        

        print('\n\nStarting Ephemeral DH exchange')

        print('\nRecieving Diffie-Hellman Step1')
        dhStep1Bytes = rsa.rsaBytesToTuple(s.recv(4096))
        dhStep1 = rsa.verifySignatureTuple(dhStep1Bytes,RsaPublicKey)
        print('received Diffie-Hellman Step1 as:',dhStep1)
        self.diffieHellman.prime = dhStep1[0]
        self.diffieHellman.generator = dhStep1[1]


        Yc = self.diffieHellman.calcKeyToShare()
        print('sending back Diffie-Hellman Public Key\n',Yc)
        dhStep2 = Yc
        sendDiffieHellmanStep2 = rsa.rsaEncrypt(dhStep2,RsaPublicKey[1],RsaPublicKey[0])

        s.send(str(sendDiffieHellmanStep2).encode())
        print('sent.')


        self.diffieHellman.key = self.diffieHellman.calcSharedPrivate(dhStep1[2])
        print('Secret key is',self.diffieHellman.key)
        