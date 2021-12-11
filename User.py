import json
from utils import *
from Crypto.Hash import SHA256

class User:
    def __init__(self, password):
        #note this will need to first decrypt file when it is enrypted
        myFile = open("information.json", "r+")
        jsonFile = json.load(myFile)
        myFile.close()

        self.name = jsonFile["user"][0]["name"]
        self.salt = jsonFile["user"][0]["salt"]
        self.email = jsonFile["user"][0]["email"]
        self.passHash = jsonFile["user"][0]["password"]
        self.pingList =  list()
        self.onlineContacts =  list()
        self.contactList = list()
        self.generateContactList(password)

    def generateContactList(self,password):
        key = generateEncrpytionHash(password, self.salt)
        decryptContacts(key)
        self.contactList.clear()
        self.onlineContacts.clear()
        
        f2 = open("contacts.json")
        f2Open = json.load(f2)
        f2.close()

       
        for contact in f2Open["contacts"]:
            self.contactList.append(contact)

        for diction in self.contactList:
            for ip in self.pingList:

                hash = SHA256.new()
                #since udpPing messages hashes email, we must validate by rehashing emails from out contact list
                hash.update(str(diction['email']).encode())
                temp = hash.hexdigest()
                #if the hashes match, add new section called IP and add to users that are online
                if temp == ip["Email"]:
                    diction["IP"] = ip["IP"]
                    diction["pubKey"] = ip["pubKey"]
                    if not diction in self.onlineContacts:
                        self.onlineContacts.append(diction)
                    else:
                      pass  
                else:
                    pass
              
        encryptContacts(key)
        self.pingList.clear()

    def getList(self):
        for item in self.contactList:
            print(item)

    def printOnlineList(self):
        print("The following contacts are online:")
        for item in self.onlineContacts:
            print("  * " + item["name"] + " <" + item["email"] + ">")

    def isContactOnline (self, email: str):
        #note that the user must use the list command first to query network
        for contact in self.onlineContacts:
            if email == contact["email"]:
                return True
        return False

    def getContact (self, email: str):
        for contact in self.onlineContacts:
            if email == contact["email"]:
                return contact
        return None




    def __del__(self):
        pass

