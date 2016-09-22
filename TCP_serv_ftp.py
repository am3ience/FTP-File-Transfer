"""
SOURCE FILE:        TCP_serv.py

PROGRAM:

DATE:               September 20, 2016

REVISIONS:          (Date and Description)

DESIGNERS:          Paul Cabanez

PROGRAMMERS:        Paul Cabanez

NOTES:

This program will accept TCP connections from machines running the client program
This "server" will send and recieve files to the above machines

"""



from socket import *
import threading
import os

# Retrieve file function
def RetrFile (name, sock):
    filename = sock.recv(1024)      # get filename from user
    if os.path.isfile(filename):    # if the file exists, and is file
        sock.send("EXISTS " + str(os.path.getsize(filename))) # get size of file
        userResponse = sock.recv(1024)      # wait for for user response
        if userResponse[:2] == 'OK':        # grab first 2 characters of response
            with open(filename, 'rb') as f: # download file (rb is read binary)
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":    # incase the file is more than 1024 bytes, give more bytes
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:                                   # if file doesn't exist
        sock.send('ERROR')

    sock.close()



myHost = ''                             # '' set default IP to localhost
myPort = 7005                           # Provided port number

s = socket(AF_INET, SOCK_STREAM)     # Create TCP socket obj
s.bind((myHost, myPort))             # bind it to server port

s.listen(5)

print("Server Started.")

while True:                             # listen until killed

    connection, address = s.accept()
    print("Client Connection at:", address)

    t = threading.Thread(target=RetrFile, args=("retrThread", connection))  #function thread
    t.start()

s.close()
