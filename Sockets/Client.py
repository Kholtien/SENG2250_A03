import socket               # Import socket module
from otherFunctions import otherFunctions as oF
import random
import hashlib
from diffieHellman import diffieHellman as dh
from RSA_A03 import rsa
from CBC_A03 import cbc
# from Cryptodome.Cipher import AES

class Client:
    def __init__(self):
        self.clientID = random.randrange(999999999)
        self.diffieHellman = dh.DiffieHellman()
        print('CLIENT')
        self.startClient()


    # def connectToServer(self):
    #     s = socket.socket()         # Create a socket object
    #     host = socket.gethostname() # Get local machine name
    #     port = 12543                # Reserve a port for your service.

    #     s.connect((host, port))
    #     self.sendHello(s)
    #     return s

    # def sendHello(self,socket):
    #     socket.send(b'Hello')

    # def closeConnection(self,socket):
    #     socket.close()

    # def killServer(self,socket):
    #     socket.send(b'closeServer')
    
    # def receiveRsaPublicKey(self,socket):
    #     print('Receiveing Public Key from Server')
    #     message = socket.recv(4096)
    #     print('public Key: ',message)
    
    def startClient(self):
        s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12543                # Reserve a port for your service.

        s.connect((host, port))
        print(s.recv(4096).decode(),'to',host)
        print('\n\nSetup Phase:\n-----------------------')
        client_hello = 'Hello'
        print('\nClient to Server:',client_hello)
        s.send(client_hello.encode())
        
        
        RsaPublicKey = rsa.rsaBytesToTuple(s.recv(4096))
        print('\nServer to Client: RSA_PK=',RsaPublicKey)
        # RsaPublicKeyString = s.recv(4096).decode()
        # RsaPublicKey = tuple(map(int, RsaPublicKeyString.replace('(','').replace(')','').split(', ')))
        # print('public Key:\n',RsaPublicKey,'\n')

        print('\n\nHandshake Phase:\n-----------------------')
        # print(self.clientID)
        print('\nClient to Server: IDc=',self.clientID)
        encryptedClientID = rsa.rsaEncrypt(self.clientID,int(RsaPublicKey[1]),int(RsaPublicKey[0]))
        # print('now sending Client ID:',self.clientID,'as',encryptedClientID)
        s.send(('IDc=' + str(encryptedClientID)).encode())
        # print('Sent Client ID\n')


        # print('\nRecieving Server_Hello')
        Server_Hello = rsa.rsaBytesToTuple(s.recv(4096))
        serverAndSID = rsa.verifySignatureTuple(Server_Hello,RsaPublicKey)
        # print('received Server_Hello as:',serverAndSID)
        serverID = serverAndSID[0]
        sid = serverAndSID[1]
        print('\nServer to Client: IDs=',serverID,'SID=',sid)
        

        print('\n\nStarting Ephemeral DH exchange')

        

        # print('\nRecieving Diffie-Hellman Step1')
        dhStep1Bytes = rsa.rsaBytesToTuple(s.recv(4096))
        dhStep1 = rsa.verifySignatureTuple(dhStep1Bytes,RsaPublicKey)
        # print('received Diffie-Hellman Step1 as:',dhStep1)
        self.diffieHellman.prime = dhStep1[0]
        self.diffieHellman.generator = dhStep1[1]

        print('\nServer to Client: \nRSASignature=',dhStep1Bytes[0],'\nDH_Prime=',dhStep1[0],'\nDH_Generator=',dhStep1[1],'\nDH_server_public_key=',dhStep1[2])
                    


        Yc = self.diffieHellman.calcKeyToShare()
        # print('sending back Diffie-Hellman Public Key\n',Yc)
        dhStep2 = Yc
        sendDiffieHellmanStep2 = rsa.rsaEncrypt(dhStep2,RsaPublicKey[1],RsaPublicKey[0])

        s.send(str(sendDiffieHellmanStep2).encode())
        print('Yc=',Yc)
        print('\nClient to Server: \nRSAEcrypted(Yc)=',sendDiffieHellmanStep2)


        self.diffieHellman.key = self.diffieHellman.calcSharedPrivate(dhStep1[2])
        print('Shared Secret key is',self.diffieHellman.key)


        print('\n\nData Exchange Phase:\n-----------------------')
        # print('receiving.')

        DEmessageClient = 'I have done it again! This message is also exactly 64 bytes wow!'
        k_ = hashlib.sha256(self.diffieHellman.key.to_bytes(1024,'big')).digest()
        # print('plainText=',DEmessageClient)
        # DErecievedMessage = s.recv(4096).decode()

        DEencryptedServer,DEhmacServer = rsa.rsaBytesToTuple(s.recv(4096))
        DEencryptedServer = DEencryptedServer.replace('\'','')
        DEhmacServer = int(DEhmacServer)
        DEmessageServer = cbc.CBCdecrypt(DEencryptedServer,k_,sid)
        calculatedHmac = int.from_bytes(cbc.hmac(k_,DEmessageServer),'big')
        print('\nServer to Client: \ncipherText=',DEencryptedServer,'\nHMAC=',DEhmacServer)

        if DEhmacServer == calculatedHmac:
            print('HMAC verified')
            print('plainText=',DEmessageServer)
        else:
            print('HMAC does not match')
            raise Exception("RSA signature does not match. Intruder Alert!")

        # print('\n\nNow sending response')
        
        # print('\nClient to Server: \nRSAEcrypted(Yc)=',dhStep2.decode())
        
        DEhmacClient = cbc.hmac(k_,DEmessageClient)
        DEcbcClient = cbc.CBCencrypt(DEmessageClient,k_,sid)
        DEtoSend = (DEcbcClient,int.from_bytes(DEhmacClient,'big'))
        print('\n\n\nplainText=',DEmessageClient)
        print('\nServer to Client: \ncipherText=',DEcbcClient,'\nHMAC=',int.from_bytes(DEhmacClient,'big'))
        # print('sending message',DEmessageClient,'as',DEtoSend)
        s.send(str(DEtoSend).encode())
        # print('sent.')
        print('Closing Connection\nConnectionClosed')
        # messageToEncrypt = 