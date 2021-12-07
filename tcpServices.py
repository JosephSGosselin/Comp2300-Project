import socket

def recieveTCP():
    port = 8888

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind(('', port))

    s.listen(5)

    try:
        while 1:
            newSocket, addr = s.accept()
            print("Contact is sending a file. Accept (y/n)?")
            while 1:
                userInput = input()
                if userInput == 'n':
                    newSocket.send('n')
                    s.close()
            else:
                pass
    finally:
        s.close()

def sendTCP():
    pass