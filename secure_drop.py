import json
import getpass
from Crypto.Cipher import AES

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

def addUser():
    myFile = open("information.json",'r+')
    jsonLoaded = json.load(myFile)

    fullName = input ("\nEnter Full Name: ")
    emailData = input ("Enter Email Address: ")
    passwordData = getpass.getpass ("Enter Password: ")
    passwordAgain = getpass.getpass ("Re-enter Password: ")

    if passwordData != passwordAgain:
        print ("\nPasswords do not match.")
        print ("Exiting SecureDrop\n")

    else:
        data = {"name":fullName,"email": emailData, "password": passwordData}
        jsonLoaded["user"].append(data)
        myFile.seek(0)
        json.dump(jsonLoaded,myFile, indent=4)
        myFile.close()
        print ("\nPasswords Match.")
        print ("User Registered.")
        print ("Exiting SecureDrop.\n")

def login():
    runLoop = True


if __name__ == "__main__":
    main()