import json
import multiprocessing
from User import User
from udpServices import *
from utils import *
from rsa import *
from tcpServices import *
from threading import *
import os

def main():

    #initalizes information.json if not created.
    try:  
        myFile = open("information.json")
    except:
        myFile = open("information.json","w+")
        myFile.write("{ \t\"user\": [] }")
        myFile.seek(0)
        print("Information.json was created...")

    jsonFile = json.load(myFile)
    myFile.close()
    registered =  (len(jsonFile["user"]) >= 1)

    if not registered:
        print ("No users are registered with this client.")
        #in this function, user will be registered, also checks for contacts.json was created
        #this is required to check for contacts since this is the first func that comes
        #in contact with the password to used to encrypt.
        registerUser()
        genRSAKeys()
    else:
        login()

def login():
    shouldLogin = False
    trys = 0
    while trys < 3 and shouldLogin != True:
        email = input("Enter Email Address: ")
        password = getpass.getpass("Enter Password: ")
        shouldLogin = verifyUser(email, password)
        trys = trys + 1
    if (shouldLogin):
        runShell(password)
    else:
        print ("To many attempts to login")
        print()
        exit()

def runShell(password):
    try:
        #loads the public key from json file
        pubKey = getPubKey()
        #when user account is made, it is taking the info from json file.
        user = User(password)
        sendProcess = multiprocessing.Process(target=sendUDP, args=(user.email, pubKey,))
        #starts thread. Dont need to join then since they are just receiving and sending udp packets
        sendProcess.start()

        tcpGet = multiprocessing.Process(target=getTCP)
        tcpGet.start()

        getProcess = multiprocessing.Process(target=getUDP, args=(user,))

    

        #giving the object of user, the process typically wont modify user
        #but with q, it is shareable memory, so i push data in the getUDP Func
        #and push it onto q, which i can then obtain the data with q.get()
        #allows me to pass pickable objects to shared memory
        q = multiprocessing.Queue()

        shouldRun = True

        #key used for decrypting and encrypting contacts
        encryptionKey = generateEncrpytionHash(password, user.salt)
        print ("Welcome to SecureDrop")
        print("Type \"help\" For Commands.")
        print()
        while (shouldRun):
            userResponse = input("secure_drop> ")
            userResponse = userResponse.lower()
            if(userResponse == "help"):
                listCommands()
            elif(userResponse == "add"):
                decryptContacts(encryptionKey)
                addContact()
                encryptContacts(encryptionKey)
                user.generateContactList(password)

            elif (userResponse == "send"):
                email = input("Email of contact: ")
                if not (user.isContactOnline(email)):
                    print ("User is not online / user is not on the contact list. Try running the list command.")
                else:
                    fileName = input("File Name?: ")
                    #still need to encrypt file first put contacts pubKey

                    #doesnt check if file exists, if it doesn't it creates an empty file and sends it
                    fileLoc = input("File Location?: ")
                    file = fileLoc+fileName
                    if os.path.exists(file):
                        sendTCP(user.getContact(email), {"email": user.email, "name": user.name, "fileName": fileName, "fileLoc": fileLoc})
                    else:
                        print("File doesn't exist")


            elif(userResponse == "list"):
                #starts to get all pings from the other clients
                getProcess = multiprocessing.Process(target=getUDP, args=(user,q))
                getProcess.start()
                #updates whole user object from getProcess
                user = q.get()
                #reloads contacts in user list() and then sees if online
                user.generateContactList(password)
                user.printOnlineList()
                getProcess.kill()
                print()
    
            elif(userResponse == "exit"):
                exit()
            else:
                print("Unknown Command")
    finally:
        tcpGet.kill()
        sendProcess.kill()
        getProcess.kill()
        del password
        del encryptionKey
    

def listCommands():
    print ("\"add\"  -> Add a new contact")
    print ("\"list\" -> List all online contacts")
    print ("\"send\" -> Transfer file to contacts")
    print ("\"exit\" -> Exit SecureDrop")


if __name__ == "__main__":
    try:
        main()
    except:
        pass