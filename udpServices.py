import socket
import time
from User import *
import multiprocessing
import json


#can send packages to the same ip/port even if multiple people are also send to that port.
def sendUDP (message: str):
    try:
        UDP_PORT = 9999
        data = message.encode()
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #on linux, this returns the correct local ip address 192.168...
        #on windows it returns the external ip address (will keep since we might need to send where packet is coming from)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        sending = True
        #if you have multi nic cards, windows will NOT broadcast to all of them. I had to Disable all but my wifi card.
        #on the linux virtual machines, it worked just fine.
        while (sending):
            jsonDumped = json.dumps({"Email": message, "IP": s.getsockname()[0]}).encode("utf-8")
            sock.sendto(jsonDumped, ('<broadcast>',UDP_PORT))
            time.sleep(.1)

    except:
        pass
    finally:
        print("\nClosed sendUDP Socket Sucessfully\n")
        sock.close()
        
#if muiltiple people running program, port isn't limited to 1 person. Multiple people can receive the UDP packages on the same port

#note do this maybe... when on List command, run this process, it will run for 2 seconds or so, and whatever is pinged back gets listed.
def getUDP (user: User, q: multiprocessing.Queue):
    UDP_IP = ""
    UDP_PORT = 9999
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


        so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        so.connect(("8.8.8.8", 80))


        sock.bind((UDP_IP, UDP_PORT))
        
        listening = True
        count = 0
        while(listening and count < 25):
            data,address = sock.recvfrom(4096)
            if str(address[0]).__eq__(str(so.getsockname()[0])) :
                count = count + 1
            elif user.pingList.__contains__(json.loads(data.decode("utf-8"))):
                count = count + 1

            else:
                try: 
                    #converts to json and stores into
                    user.pingList.append(json.loads(data.decode("utf-8")))
                    count = count + 1
                except:
                    pass
            
            
   
    except:
        pass
    finally:
        #when finally block enters, push the update user onto shared Memory and finsih up closing
        sock.close()
        q.put(user)
        #print("Closed getUDP Socket Sucessfully\n")
 
