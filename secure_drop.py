import json
import getpass
from Crypto.Cipher import AES

from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import bcrypt, bcrypt_check


def main():
    myFile = open("information.json")
    jsonFile = json.load(myFile)
    myFile.close()

    registered =  (len(jsonFile["user"]) >= 1)

    if not registered:
        print ("No users are registered with this client.")
        registerUser()
    else:
        login()

def registerUser():
    runLoop = True
    while runLoop:
        userResponse = input("Would you like to register a user (y/n)? ")
        if (userResponse.lower() != "y") and (userResponse.lower() != "n"):
            print ("invalid response...\n")
        else:
            if userResponse.lower() == 'y':
                addUser()
                runLoop = False
            else:
                print ("Exiting User Registration\n")
                runLoop = False

def generateHash(passwordString):
    password = str(passwordString).encode()
    b64pwd = b64encode(SHA256.new(password).digest())
    return bcrypt(b64pwd,12)

def verifyPassword(password, hash1):
    try:
        b64pwd = b64encode(SHA256.new(str(password).encode()).digest())
        inBytes = str(hash1).encode()
        bcrypt_check(b64pwd,str(hash1).encode())
        return True
    except:
        print()
 
def addUser():
    myFile = open("information.json",'r+')
    jsonLoaded = json.load(myFile)

    fullName = input ("\nEnter Full Name: ")
    emailData = input ("Enter Email Address: ")
    passwordData =  getpass.getpass ("Enter Password: ")
    passwordAgain = getpass.getpass ("Re-enter Password: ")

    if passwordData != passwordAgain:
        print ("\nPasswords do not match.")
        print ("Exiting SecureDrop\n")

    else:
        data = {"name":fullName,"email": emailData, "password": generateHash(passwordData).decode() test,"Contacts":[] }
        jsonLoaded["user"].append(data)
        myFile.seek(0)
        json.dump(jsonLoaded,myFile, indent=4)
        myFile.close()
        print ("\nPasswords Match.")
        print ("User Registered.")
        print ("Exiting SecureDrop.\n")
def addContact(password):
    myFile = open("information.json",'r+')
    jsonLoaded = json.load(myFile)
    contactName = input("Enter Full Name: ")
    contactEmail = input ("Enter Email Address: ")


    data = {"name":contactName,"email":contactEmail}
    jsonLoaded["user"][0]["Contacts"].append(data)
    myFile.seek(0)
    json.dump(jsonLoaded,myFile, indent=4)
    myFile.close()

def verifyUser(email,password):
    myFile = open("information.json",'r')
    jsonLoaded = json.load(myFile)
    for user in jsonLoaded["user"]:
        if user["email"] == email:
            if verifyPassword(password, user["password"]):
                return True
    print ("Incorrect Password/Email Combination\n")
    return False     

def listCommands():
    print ("\"add\"  -> Add a new contact")
    print ("\"list\" -> List all online contacts")
    print ("\"send\" -> Transfer file to contacts")
    print ("\"exit\" -> Exit SecureDrop")

def runShell(password):
    shouldRun = True
    print ("Welcome to SecureDrop")
    print("Type \"help\" For Commands.")
    print()
    while (shouldRun):
        userResponse = input("secure_drop> ")
        userResponse = userResponse.lower()
        if(userResponse == "help"):
            listCommands()
        elif(userResponse == "add"):
            addContact(password)
        elif (userResponse == "send"):
            print("sending")
        elif(userResponse == "list"):
            print("listing")
        elif(userResponse == "exit"):
            exit()
        else:
            print("Unknown Command")

    



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


if __name__ == "__main__":
    main()