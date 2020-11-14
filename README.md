# SENG2250 A03

requires the installation of pycryptodomex

you can do this by `pip3 install pycrytpodomex` (or `pip install pycryptodomex` depending on your PATH settings)

This demonstration required two instances of a terminal from which to run python.

In the first terminal, once in the directory, run the command `python ./A03.py s` to start the server instance.

Wait up to 10 seconds for the server to initialize, it is calculating the information for the RSA connection. Once you see `Waiting for connection.` then proceed

In the second terminal, once in the directory, run the command `python ./A03.py c` to start the client. 

This will connect the two terminals and the program will run through a setup phase, SSL handshake phase, then a data excahnge phase. 

Once this is complete, the server will continue to run until exited and the client will disconnect from the server. 

You can now run `python ./A03.py c` again to run another instance of the client. 
