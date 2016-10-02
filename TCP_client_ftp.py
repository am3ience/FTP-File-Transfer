"""
SOURCE FILE:        TCP_client.py

PROGRAM:

DATE:               September 20, 2016

REVISIONS:          (Date and Description)

                    September 23, 2016
                    finished basic functionality

                    September 30, 2016
                    finished commenting

DESIGNERS:          Paul Cabanez

PROGRAMMERS:        Paul Cabanez

NOTES:

This program will connect to the TCP server
This program will send and recieve files from the server

"""

from socket import *
import sys
import os

servHost = ''                           # '' set default IP to localhost
servPort = 7005                         # Provided port number

s = socket(AF_INET, SOCK_STREAM)        # Create TCP socket obj
s.connect((servHost, servPort))         # bind it to server port

# ask user for send or retrieve
decision = raw_input("do you want to send or retrieve a file?(send/retrieve): ")
s.send(decision) # sends the decision to the server

# if user picks retrieve
if decision == "retrieve" or decision == "Retrieve":
    filename = raw_input("Filename of file you want to retrieve from server: ")   # ask user for filename
    if filename != "q":                     # a way out
        s.send(filename)                    # send filename to server
        data = s.recv(1024)                 # check if data is recieved
        if data[:6] == 'EXISTS':            # checks first 6 chars of data to see if it exists
            filesize = long(data[6:])       # get filesize, which is after the 6 chars + onwards
            message = raw_input("File Exists, " + str(filesize)+"Bytes, download?: Y/N -> ")    # ask the user if they want to download

            if message == "Y" or message == "y":
                s.send('OK')                            # send response to server
                f = open('new_' + filename, 'wb')       # creates the file with "new_" in the beginning
                data = s.recv(1024)                     # recieve data
                totalRecieved = len(data)               # get length of data
                f.write(data)
                while totalRecieved < filesize:         # if there's more than 1024 bytes of data, add more
                    data = s.recv(1024)
                    totalRecieved += len(data)
                    f.write(data)
                    print("{0: .2f}".format((totalRecieved/float(filesize))*100)) + "% Done" # print % of download progress

                print("Download Done!")

        else:
            print("File does not exist!")
    s.close()

# if user picks send
elif decision == "send" or decision == "Send":
    print("List of files in current directory: ")   # prints files in current directory
    print(os.listdir("."))
    filename = raw_input("Filename of file you want to send to server: ") # ask user filename on server
    if filename != "q":                     # way out
        s.send(filename)                    # send filename to server
        if os.path.isfile(filename):        # checks if the file exists, and is file
            s.send("EXISTS " + str(os.path.getsize(filename))) # get size of file
            userResponse = s.recv(1024)      # wait for for user response
            if userResponse[:2] == 'OK':
                with open(filename, 'rb') as f: # download file (rb is read binary)
                    bytesToSend = f.read(1024)
                    s.send(bytesToSend)
                    while bytesToSend != "":    # incase the file is more than 1024 bytes, give more bytes
                        bytesToSend = f.read(1024)
                        s.send(bytesToSend)
        else:                                   # if file doesn't exist
            s.send('ERROR')

    s.close()


s.close()
