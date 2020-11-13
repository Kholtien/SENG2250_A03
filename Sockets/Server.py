import socket               # Import socket module
from otherFunctions import otherFunctions as oF
import random
import hashlib
from diffieHellman import diffieHellman as dh
from RSA_A03 import rsa
from Cryptodome.Cipher import AES

class Server:
    def __init__(self):
        self.ServerID = random.randrange(999999999)
        self.RSA = rsa.RSA()
        self.diffieHellman = dh.DiffieHellman()
        self.diffieHellman.prime =      178011905478542266528237562450159990145232156369120674273274450314442865788737020770612695252123463079567156784778466449970650770920727857050009668388144034129745221171818506047231150039301079959358067395348717066319802262019714966524135060945913707594956514672855690606794135837542707371727429551343320695239
        self.diffieHellman.generator =  174068207532402095185811980123523436538604490794561350978495831040599953488455823147851597408940950725307797094915759492368300574252438761037084473467180148876118103083043754985190983472601550494691329488083395492313850000361646482644608492304078721818959999056496097769368017749273708962006689187956744210730
        

        while self.RSA.p == self.RSA.q:                   #Make sure that P and Q are not equal
            self.RSA.q = oF.generate_prime_number(1024)

        print ('e Value:',self.RSA.e,'\n')
        print ('RSA Prime 1:',self.RSA.p,'\n')
        print ('RSA Prime 2:',self.RSA.q,'\n')
        print ('Modulus:',self.RSA.n,'\n')
        print ('Public Key:',self.RSA.publicKey,'\n')

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
                try:
                    message = conn.recv(4096)
                except:
                    break
                
                if      message == b'Hello':
                    print('received',message.decode())
                    print('Now Sending RSA Public Key')
                    conn.send(str(self.RSA.publicKey).encode())
                    print('Sent RSA Public Key')
                elif      message.decode()[0:3] == 'IDc':
                    print('receiving Client_Hello')
                    print('Received',message.decode()[0:len(message.decode())])
                    encryptedClientID = int(message.decode()[5:len(message.decode())])
                    clientID = rsa.rsaDecrypt(encryptedClientID,self.RSA.d,self.RSA.n)
                    print(clientID)
                    

                    print('\nGenerating SID')
                    SID = random.randrange(999999999)
                    while SID == self.ServerID:
                        SID = random.randrange(999999999)
                    print('SID:',SID)

                    # rsaSignatureHash = hashlib.sha256(str((self.ServerID,SID)).encode())
                    # rsaSignatureHashInt = int('0x'+rsaSignatureHash.hexdigest(),16)
                    # server_Hello = (rsa.rsaEncrypt(rsaSignatureHashInt,self.RSA.d,self.RSA.n),self.ServerID,SID)
                    server_Hello = rsa.tupleToRsaSignatureAndTuple((self.ServerID,SID),self.RSA.d,self.RSA.n)

                    print('sending Server_Hello')
                    conn.send(str(server_Hello).encode())

                    print('\n\nStarting Ephemeral DH exchange')
                    Ys = self.diffieHellman.calcKeyToShare()
                    print('Sent.')


                    dhStep1 = (self.diffieHellman.prime,self.diffieHellman.generator,Ys)
                    sendDiffieHellman1 = rsa.tupleToRsaSignatureAndTuple(dhStep1,self.RSA.d,self.RSA.n)

                    print('\nSending Diffie Hellman Step 1',dhStep1)
                    conn.send(str(sendDiffieHellman1).encode())
                    print('Sent.')
                    
                    print('\nRecieving Diffie-Hellman Step 2')
                    dhStep2 = conn.recv(4096)
                    Yc = rsa.rsaDecrypt(int(dhStep2.decode()),self.RSA.d,self.RSA.n)
                    print('Received:\n',Yc)

                    self.diffieHellman.key = self.diffieHellman.calcSharedPrivate(Yc)
                    print('Secret key is',self.diffieHellman.key)


                elif not message:
                    break
                else:
                    print('no match on message')

            conn.close()