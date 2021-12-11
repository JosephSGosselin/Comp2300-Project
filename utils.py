import json
import getpass
import string
import random
from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import bcrypt, bcrypt_check, PBKDF2
from User import *

#used for password verification
def generateHash(passwordString):
    password = str(passwordString).encode()
    b64pwd = b64encode(SHA256.new(password).digest())
    return bcrypt(b64pwd,12)

#used to add first user, not the contacts thats different
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
        generatedSalt = get_random_string(32)
        data = {"name":fullName,"email": emailData, "password": generateHash(passwordData).decode(),"salt": generatedSalt }
        jsonLoaded["user"].append(data)
        myFile.seek(0)
        json.dump(jsonLoaded,myFile, indent=4)
        myFile.close()

        encryptionKey = generateEncrpytionHash(passwordData, generatedSalt)

        #if file exist, great move on
        try:  
            myFile = open("contacts.json")
        except:
            #if not, create the template and finish
            myFile = open("contacts.json","w+")
            myFile.write("{ \t\"contacts\": [] }")
            myFile.seek(0)
            print("\ncontacts.json was created and encrypted...")

        encryptContacts(encryptionKey)
        myFile.close()
        del encryptionKey
        del passwordData
        del passwordAgain


        print ("\nPasswords Match.")
        print ("User Registered.")
        print ("Exiting SecureDrop.\n")

#this is used to generate an ascii salt of any length
def get_random_string(length):
    letters = string.ascii_lowercase + string.ascii_uppercase + "0123456789"
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

#used to login
def verifyUser(email,password):
    myFile = open("information.json",'r')
    jsonLoaded = json.load(myFile)
    for user in jsonLoaded["user"]:
        if user["email"] == email:
            if verifyPassword(password, user["password"]):
                return True
    print ("Incorrect Password/Email Combination\n")
    return False

#when login, check the stored hashed password with the attempted sign in password
def verifyPassword(password, hash1):
    try:
        b64pwd = b64encode(SHA256.new(str(password).encode()).digest())
        bcrypt_check(b64pwd,str(hash1).encode())
        return True
    except:
        print()

#used to shorten/make longer someones password, and hashed to 256 bits
#this will be used to encrpyted using AES
def generateEncrpytionHash (password, storedSalt):
    salt = str(storedSalt).encode()
    key = PBKDF2(password,salt,32)
    return key

def addContact():
    myFile = open("contacts.json",'r+')
    jsonLoaded = json.load(myFile)
    contactName = input("Enter Full Name: ")
    contactEmail = input ("Enter Email Address: ")
    data = {"name":contactName,"email":contactEmail}
    Contacts = jsonLoaded["contacts"]

    #updates contacts if needed
    shouldAppend = True
    for contact in Contacts:
        if str(contact["email"]).__eq__(contactEmail):
            contact["name"] = contactName
            print("Contact Updated\n")
            shouldAppend = False
    if shouldAppend:
        Contacts.append(data)
        print("Contact Added")
    # if Contacts == []:
    #     Contacts.append(data)
    #     print ("Contact added.\n")
    # elif contactEmail in [x["email"] for x in Contacts]:
    #     count = 0
    #     for x in range(0,len(Contacts)):
    #         if Contacts[x]["email"] == contactEmail:
    #             count = x
    #     Contacts[x]["name"] = contactName
    #     print(Contacts[x]["name"])
    #     print ("Contact updated.\n")
    # else:
    #     Contacts.append(data)
    #     print ("Contact added.\n")

    myFile.seek(0)
    json.dump(jsonLoaded,myFile, indent=4)
    myFile.close()

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

def encryptContacts (key):
    #gets data, clears file, closes.
    myFile = open("contacts.json","r+")
    data = ""
    for i in myFile:
        data+=i

    #clears file aso it gets ready for the encrypted data
    myFile.truncate(0)
    myFile.close()

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())

    #reopens file with correct mode for encryption
    file_out = open("contacts.json","wb")
    [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    file_out.close()

def decryptContacts (key):
    #opens the encrypted contacts
    #reads in 3 items to verify and decrypt
    myFile = open("contacts.json","rb")
    nonce, tag, ciphertext = [ myFile.read(x) for x in (16, 16, -1) ]
    myFile.close()

    cipher = AES.new(key, AES.MODE_EAX, nonce)

    #if can decrypt suceffully then do so
    try:

        data = cipher.decrypt_and_verify(ciphertext, tag)
    except:
        #deletes contacts if validity not there.
        print("Contact Verification failed...\nClearing Contacts for Saftey...\nExiting...\n")
        myFile = open("contacts.json","r+")
        myFile.truncate(0)
        myFile.write("{\n\t\"contacts\": [] \n}")
        myFile.seek(0)
        encryptContacts(key)
        exit()
   
    #if the file was not tampered with, decrypt and store data normally.
    myFile = open("contacts.json","r+")
    myFile.truncate(0)
    myFile.write(data.decode())


