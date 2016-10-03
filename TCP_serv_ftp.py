"""
SOURCE FILE:        TCP_serv_FTP.py

PROGRAM:			TCP_serv_FTP

DATE:               September 20, 2016

REVISIONS:          (Date and Description)

                    September 23, 2016
                    finished basic functionality, need to figure out a way for
                    connection to be able to be used by both retrieve and send
                    functions

                    September 27, 2016
                    made if statements on server in while loop, will get decision
                    from client to either send or retrieve. It all works now.

                    September30, 2016
                    finished commenting



DESIGNERS:          Paul Cabanez

PROGRAMMERS:        Paul Cabanez

NOTES:

Make sure to start this script first before the client 
This program will accept TCP connections from machines running the client program and
will retrieve and send files as requested from the client


"""



from socket import *
from thread import *
import threading
import os


# Send file function
def SendFile (name, sock):
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

# retrieve file function
def RetrFile (name, sock):
    filename = sock.recv(1024)      # get filename from user
    data = sock.recv(1024)          # recieve data
    if data[:6] == 'EXISTS':            # checks first 6 chars of data to see if it exists
        filesize = long(data[6:])       # get filesize, which is after the 6 chars + onwards
        sock.send('OK')
        f = open('new_' + filename, 'wb')       # creates the file with "new_" in the beginning
        data = sock.recv(1024)
        totalRecieved = len(data)               # get length of data
        f.write(data)
        while totalRecieved < filesize:         # if there's more than 1024 bytes of data, add more
            data = sock.recv(1024)
            totalRecieved += len(data)
            f.write(data)

    sock.close()

myHost = ''                             # '' set default IP to localhost
myPort = 7005                           # Provided port number

s = socket(AF_INET, SOCK_STREAM)     # Create TCP socket obj
s.bind((myHost, myPort))             # bind it to server port

s.listen(5)                         #up to 5 connections

print("Server Started.")

while True:                             # listen until killed

    connection, address = s.accept()
    print("Client Connection at:", address)

    decision = connection.recv(1024)    # gets send/retrieve decision from client

    if decision == "retrieve" or decision == "Retrieve":    # retrieve function thread
        start_new_thread(SendFile,("sendThread",connection,))


    elif decision == "send" or decision == "Send":          # send function thread 
        start_new_thread(RetrFile,("retrThread",connection,))

s.close()
