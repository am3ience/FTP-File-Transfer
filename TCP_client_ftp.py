"""
SOURCE FILE:        TCP_client.py

PROGRAM:

DATE:               September 20, 2016

REVISIONS:          (Date and Description)

DESIGNERS:          Paul Cabanez

PROGRAMMERS:        Paul Cabanez

NOTES:

This program will connect to the TCP server
This program will send and recieve files to the server

"""

from socket import *
import sys

servHost = ''                           # '' set default IP to localhost
servPort = 7005                         # Provided port number

s = socket(AF_INET, SOCK_STREAM)        # Create TCP socket obj
s.connect((servHost, servPort))         # bind it to server port

filename = raw_input("Filename: ")      # ask user for filename

if filename != "q":                     # a way out
    s.send(filename)                    # send filename to server
    data = s.recv(1024)                 # check if data is recieved
    if data[:6] == 'EXISTS':            # checks first 6 chars of data to see if it exists
        filesize = long(data[6:])       # get filesize, which is after the 6 chars + onwards
        message = raw_input("File Exists, " + str(filesize)+"Bytes, download?: Y/N -> ")    # ask the user if they want to download

        if message == "Y" or message == "y":
            s.send('OK')
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






s.close()
