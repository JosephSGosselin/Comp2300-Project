import socket
import json
def getTCP():
    port = 9998
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind(('', port))
    BUFSIZE = 4098

    s.listen(5)

    try:
        while True:
            client, addr = s.accept()
            #loads into json format
            senderInfo = json.loads(client.recv(BUFSIZE).decode())
            print("\nContact " + senderInfo["name"] + "<" + senderInfo["email"] +"> is sending a file named \"" + senderInfo["fileName"]+"\"")
            client.send("Name Received".encode())

            #reads in all data coming in until no more
            with open(senderInfo["fileName"], "w+") as file:
                while True:
                    data = client.recv(BUFSIZE).decode()
                    if not data:
                        #meaning nothing was transmitted:
                        break
                    file.write(data)
            client.send("File Data Received".encode())
            print("File received Succesfully...")
            print('secure_drop>')
            client.close()

    finally:
        print("TcpGET Closed")
        s.close()

def sendTCP(listObj: dict, sendInfo: dict ):
    BUFSIZE = 4098
    host = listObj["IP"]
    port = 9998
    data = ""
    try:
        s = socket.socket()
        s.connect((host,port))
        jsonDump = json.dumps(sendInfo)
        s.send(jsonDump.encode())
        s.recv(BUFSIZE)

        loc = str(sendInfo["fileLoc"])

        #if user forgets to add the last slash in the file path
        if  not( loc.endswith('\\') or loc.endswith('\/') ):
            loc += "\/"
        loc += sendInfo["fileName"]
        with open(loc,"w+") as file:
            while True:
                data = file.readline()
                if not data:
                    break       
                s.send(data.encode())
            print ("File sent...")
    finally:
        #sending file content
        s.close()

        