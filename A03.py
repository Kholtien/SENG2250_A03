import socket               # Import socket module
from otherFunctions import otherFunctions
from Sockets import Client
from Sockets import Server
import sys

if len(sys.argv) > 1:
    clinetOrServer = sys.argv[1]
    if      clinetOrServer.lower() == 'c' or clinetOrServer.lower() == 'client':
        client = Client.Client()
        # clientConn = client.connectToServer()
        # # client.sendHello(clientConn)
        # client.receiveRsaPublicKey(clientConn)
        # client.killServer(clientConn)
        # client.closeConnection(clientConn)
    elif    clinetOrServer.lower() == 's' or clinetOrServer.lower() == 'server':
        Server.Server()
    else:
        print("Please use argument 'c' for client or 's' for server")
else:
    print("Please use argument 'c' for client or 's' for server")
