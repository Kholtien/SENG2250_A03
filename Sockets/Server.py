import socket               # Import socket module
from otherFunctions import otherFunctions as oF
import random

class Server:
    def __init__(self):
        self.ServerID = random.randrange(999999999)
        self.RsaE = 65537 #Public Key
        self.RsaP = oF.generate_prime_number(1024)      #RSA prime 1
        self.RsaQ = oF.generate_prime_number(1024)      #RSA prime 2
        self.RsaN = self.RsaP * self.RsaQ               #n or modulus
        self.totient = (self.RsaP - 1) * (self.RsaQ - 1)#Totient
        self.RsaD = oF.findModInverse(self.RsaE,self.totient)
        self.publicKey = (self.RsaN,self.RsaE)
        self.privateKey = (self.RsaN,self.RsaD)
        
        while self.RsaP == self.RsaQ:                   #Make sure that P and Q are not equal
            self.RsaQ = oF.generate_prime_number(1024)

        print ('e Value:',self.RsaE,'\n')
        print ('RSA Prime 1:',self.RsaP,'\n')
        print ('RSA Prime 2:',self.RsaQ,'\n')
        print ('Modulus:',self.RsaN,'\n')
        print ('Public Key:',self.publicKey,'\n')

        self.serverSocket = self.startServer()


    def startServer(self):
        s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12543                # Reserve a port for your service.
        s.bind((host, port))        # Bind to the port

        s.listen(5)                 # Now wait for client connection.

        
        while True:
            print('\n\nWaiting For Connection\n')
            conn, addr = s.accept()
            print('Got connection from', addr)
            conn.send(b'Thank you for connecting')

            while True:
                #receive message
                message = conn.recv(4096)
                if      message == b'Hello':
                    print('received',message.decode())
                    print('Now Sending RSA Public Key')
                    conn.send(str(self.publicKey).encode())
                    print('Sent RSA Public Key')
                elif      message.decode()[0:3] == 'IDc':
                    print('receiving Client_Hello')
                    print('Received',message.decode()[0:len(message.decode())])
                    encryptedClientID = int(message.decode()[5:len(message.decode())])
                    clientID = oF.powmod(encryptedClientID,self.RsaD,self.RsaN)
                    print(clientID)
                    conn.send(self.ServerID.to_bytes(1024,byteorder='big'))
                    print('sending Server_Hello')
                elif not message:
                    break
                else:
                    print('no match on message')

            conn.close()

            

#        while True:
#            c, addr = s.accept()     # Establish connection with client.
#            print('Got connection from', addr)
#            c.send(b'Thank you for connecting')
#            message = c.recv(1024).decode('ascii')
#            data = self.receiveMessage(message,c)
#            print(data)
#            if data == 'closeServer':
#                c.close()
#                break
#            #c.close()                # Close the connection

        return s