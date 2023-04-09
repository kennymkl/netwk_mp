def printFromServer(bytesAddressPair):
    convMsg = str(bytesAddressPair[0], encoding)
    jsonMsg = json.loads(convMsg)
    serverMsg = "\n{}".format(jsonMsg["message"])
    print(serverMsg)

def joinComm(userCommand):
    
    try:
        wholeCommand = str.split(userCommand," ")
        jsonFormat =  { "command":wholeCommand[0]}

        # convert into JSON:
        y = json.dumps(jsonFormat)
        bts = str.encode(y)                                 # Bytes to Send
        sap = (wholeCommand[1], int(wholeCommand[2]))       # Server Address Port

        print(sap)

        return bts, sap
    except:
        print("Error: Command parameters do not match or is not allowed.")

def leaveComm(userCommand):
    jsonFormat =  { "command":userCommand}

    # convert into JSON:
    y = json.dumps(jsonFormat)
    bytesToSend = str.encode(y)

    return bytesToSend

def regComm(userCommand):
    wholeCommand = str.split(userCommand," ")
    jsonFormat =  { "command":wholeCommand[0], "handle":wholeCommand[1]}

    # convert into JSON:
    y = json.dumps(jsonFormat)
    bts = str.encode(y)                                 # Bytes to Send

    return bts

def msgComm(userCommand):
    wholeCommand = str.split(userCommand," ",2)
    print(wholeCommand)
    jsonFormat =  { "command":wholeCommand[0], "handle":wholeCommand[1], "message":wholeCommand[2]}

    # convert into JSON:
    y = json.dumps(jsonFormat)
    bts = str.encode(y)                                 # Bytes to Send

    return bts

def allComm(userCommand):
    wholeCommand = str.split(userCommand," ",1)
    jsonFormat =  { "command":wholeCommand[0], "message":wholeCommand[1]}

    # convert into JSON:
    y = json.dumps(jsonFormat)
    bts = str.encode(y)                                 # Bytes to Send

    return bts

import socket
import threading
import json
import time

encoding = 'utf-8'
bufferSize = 1024          
global serverAddressPort
joined = False


# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)



while (joined==False):
    userStartCommand = input("Enter command: ")
    if "/join" in userStartCommand:
        try:
            bytesToSend, serverAddressPort = joinComm(userStartCommand)

            # Send to server using created UDP socket
            print(serverAddressPort)
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            joined = True

        except:
            print("Error: Connection to the Message Board Server has failed!")
            print("Please check IP Address and Port Number")
    else:
        print("Error: Command not found.")



# Listen for incoming datagrams
def sender():
    global serverAddressPort
    global joined

    while(joined):
        userCommand = input("Enter command: ")

        if "/join" in userCommand:
            try:
                joined = True
                bytesToSend, serverAddressPort = joinComm(userCommand)

                # Send to server using created UDP socket
                UDPClientSocket.sendto(bytesToSend, serverAddressPort)

            except:
                print("Error: Connection to the Message Board Server has failed!")
                print("Please check IP Address and Port Number")


        elif "/leave" in userCommand:
            if joined:
                #UDPClientSocket.close() # close the socket
                bytesToSend = leaveComm(userCommand)
                UDPClientSocket.sendto(bytesToSend, serverAddressPort)
                joined = False  # set joined flag to False
                
                break
            else:
                print("Error: Disconnection failed. Please connect to the server first.")

            
        elif "/register" in userCommand:
            bytesToSend = regComm(userCommand)
            # Send to server using created UDP socket
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        elif "/msg" in userCommand:
            bytesToSend = msgComm(userCommand)
            # Send to server using created UDP socket
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        elif "/all" in userCommand: 
            bytesToSend = allComm(userCommand)
            # Send to server using created UDP socket
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        elif "/?" in userCommand:
            print("------COMMANDS ------")
            print("Connect to the server application: /join <server_ip_add> <port>")
            print("Disconnect to the server application: /leave")
            print("Register a unique handle or alias: /register <handle>")
            print("Send message to all: /all <message>")
            print("Send direct messages to a single handle: /msg <handle> <message>")
            print("Request command help  to ouptut all input syntax commands for references: /?")
            print("----------------------------")
            print(" ")
            
        else:
            print("Error: Command not found.")

        time.sleep(1)

def receiver():

    while(True):
        bytesAddressPair = UDPClientSocket.recvfrom(bufferSize) # Receive from Server a tuple (bytes, address)
        printFromServer(bytesAddressPair)

receive = threading.Thread(target=receiver)
send = threading.Thread(target=sender)

if (joined==True):
    print("Thread started")
    receive.start()
    send.start()