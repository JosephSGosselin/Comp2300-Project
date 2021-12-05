import json
import multiprocessing
from User import User
from udpServices import *
from utils import *
import string


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

    #when user account is made, it is taking the info from json file.
    user = User(password)
    sendProcess = multiprocessing.Process(target=sendUDP, args=(user.email,))

    #getProcess = multiprocessing.Process(target=getUDP, args=(user,)
    #starts thread. Dont need to join then since they are just receiving and sending udp packets
    sendProcess.start()
   

    #giving the object of user, the process typically wont modify user
    #but with q, it is shareable memory, so i push data in the getUDP Func
    #and push it onto q, which i can then obtain the data with q.get()
    #allows me to pass pickable objects to shared memory
    q = multiprocessing.Queue()


   
    shouldRun = True
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
            print("sending")
        elif(userResponse == "list"):
            print("Pinging Contacts...")
            getProcess = multiprocessing.Process(target=getUDP, args=(user,q))
            getProcess.start()
            #updates whole user object from getProcess
            user = q.get()
            user.generateContactList(password)
            getProcess.kill()
            print()
  
        elif(userResponse == "exit"):
            del password
            del encryptionKey
            sendProcess.kill()
            exit()
        else:
            print("Unknown Command")

    

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