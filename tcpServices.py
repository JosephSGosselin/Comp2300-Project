import socket

def getTCP():
    port = 8888

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind(('', port))

    s.listen(5)

    try:
        while True:
            client, addr = s.accept()
            print("Contact is sending a file. Accept (y/n)?")
            userInput = input()

            if userInput == 'n':
                client.send('n')
                s.close()
                break
            elif userInput == 'y':
                break

    finally:
        s.close()

def sendTCP(listObj: dict):
    print ("inside")
    host = listObj["IP"]
    port = 8888
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host,port))

        