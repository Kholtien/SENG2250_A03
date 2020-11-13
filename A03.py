from sys        import argv
from Sockets    import Client
from Sockets    import Server


if len(argv) > 1:
    clinetOrServer = argv[1]
    if      clinetOrServer.lower() == 'c' or clinetOrServer.lower() == 'client':
        client = Client.Client()
    elif    clinetOrServer.lower() == 's' or clinetOrServer.lower() == 'server':
        Server.Server()
    else:
        print("Please use argument 'c' for client or 's' for server")
else:
    print("Please use argument 'c' for client or 's' for server")
