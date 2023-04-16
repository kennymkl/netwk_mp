import socket
import json


def msgToClient(msgFromServer):
    jsonFormat =  {"message":msgFromServer}
    y = json.dumps(jsonFormat)           # convert into JSON:
    bts = str.encode(y)

    return bts

encoding = 'utf-8'

localIP     = "127.0.0.1"
localPort   = 12345
bufferSize  = 1024

# variables
handles = []
global destAddr

msgFromServer = ""
jsonFormat =  {"message":msgFromServer}
y = json.dumps(jsonFormat)           # convert into JSON:
bytesToSend = str.encode(y)

# Create a datagram socket
UDPserver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPserver.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
while(True):

    bytesAddressPair = UDPserver.recvfrom(bufferSize)               # Receive from Server a tuple (bytes, address)
    address = bytesAddressPair[1]
    convMsg = str(bytesAddressPair[0], encoding)                    # Convert message from bytes to str
    jsonMsg = json.loads(convMsg)                                   # Parse str to json

    if jsonMsg["command"] == "/join":
        bytesToSend = msgToClient("Connection to the Message Board Server is successful!")

        # Sending a reply to client
        UDPserver.sendto(bytesToSend, address)

    elif jsonMsg["command"] == "/leave":
        bytesToSend = msgToClient("Connection closed. Thank you!")

        # Sending a reply to client
        UDPserver.sendto(bytesToSend, address)
        print("A connection closed.")

    elif jsonMsg["command"] == "/register":
        if (len(handles) == 0):
            handles.append({'handle' : jsonMsg["handle"], 'addr' : address})
            msgFromServer = "Welcome " + jsonMsg["handle"] + "!"
            bytesToSend = msgToClient(msgFromServer)
            print(handles)
        else:
            if any(d['handle'] == jsonMsg["handle"] for d in handles):
                bytesToSend  = msgToClient("Error: Registration failed. Handle or alias already exists.")
            else:
                handles.append({'handle' : jsonMsg["handle"], 'addr' : address})
                msgFromServer = "Welcome " + jsonMsg["handle"] + "!"
                bytesToSend = msgToClient(msgFromServer)
                print(handles)
            
        # Sending a reply to client
        UDPserver.sendto(bytesToSend, address)

    elif jsonMsg["command"] == "/msg":
        if any(d['handle'] == jsonMsg["handle"] for d in handles):
            destList = next(x for x in handles if x["handle"] == jsonMsg["handle"])
            destAddr=destList['addr']

            srcList = next(x for x in handles if x["addr"] == address)
            srcHandle = srcList['handle']

            msgFromSrcClient = jsonMsg["message"]
            bytesToSendDest = msgToClient("\n[From " + srcHandle + "]: " + msgFromSrcClient + "\nEnter command: ")
            bytesToSendsource = msgToClient("\n[To " + jsonMsg["handle"] + "]: " + msgFromSrcClient)

            # Sending a reply to destination client
            UDPserver.sendto(bytesToSendDest, destAddr)
            # Sending a reply to source client
            UDPserver.sendto(bytesToSendsource, address)
        else:
            bytesToSend = msgToClient("Error: Handle or alias not found.")
            UDPserver.sendto(bytesToSend, address)

    elif jsonMsg["command"] == "/all":

        srcList = next(x for x in handles if x["addr"] == address)
        srcHandle = srcList['handle']
        msgFromSrcClient = jsonMsg["message"]

        bytesToSend = msgToClient("\n" + srcHandle + ": " + msgFromSrcClient) #+ "\nEnter command: ")

        for x in handles:
            destAddr = x["addr"] 
             # Sending a reply to destination clients
            UDPserver.sendto(bytesToSend, destAddr)


    