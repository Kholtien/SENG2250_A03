import socket               # Import socket module
from otherFunctions import otherFunctions
from Sockets import Client
from Sockets import Server
import sys

if len(sys.argv) > 1:
    clinetOrServer = sys.argv[1]
    if      clinetOrServer.lower() == 'c' or clinetOrServer.lower() == 'client':
        client = Client.Client()
        client.connectToServer()
        #client.sendHello(c)
        client.killServer(client)
        client.closeConnection(client)
    elif    clinetOrServer.lower() == 's' or clinetOrServer.lower() == 'server':
        Server.Server()
    else:
        print("Please use argument 'c' for client or 's' for server")
else:
    print("Please use argument 'c' for client or 's' for server")
