import socket               # Import socket module
from otherFunctions import otherFunctions as oF

class Server:
    def __init__(self):
        self.publicKey = 65537
        self.RsaP = oF.generate_prime_number(2048)
        self.RsaQ = oF.generate_prime_number(2048)
        self.startServer()


    def receiveMessage(self,message,client):
        if      message.lower() == 'hello':
            print('received ',message)
        elif    message.lower() == 'closeserver':
            return message

    def startServer(self):
        s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12345                # Reserve a port for your service.
        s.bind((host, port))        # Bind to the port

        s.listen(5)                 # Now wait for client connection.
        while True:
            c, addr = s.accept()     # Establish connection with client.
            print('Got connection from', addr)
            c.send(b'Thank you for connecting')
            message = c.recv(1024).decode('ascii')
            data = self.receiveMessage(message,c)
            print(data)
            if data == 'closeServer':
                c.close()
                break
            #c.close()                # Close the connection