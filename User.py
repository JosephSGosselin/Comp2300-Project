import json
from utils import *
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

        f2 = open("contacts.json")
        f2Open = json.load(f2)
        f2.close()

        for contact in f2Open["contacts"]:
            self.contactList.append(contact)
        for diction in self.contactList:
            for ip in self.pingList:
                if str(diction["email"]).__eq__(str(ip["Email"])):
                    print(diction)
                    diction["IP"] = ip["IP"]
                    if not(self.onlineContacts.__contains__(diction["IP"])):
                        self.onlineContacts.append(diction)
                    else:
                      pass  
                else:
                    pass
        self.pingList.clear()
        encryptContacts(key)

    def getList(self):
        for item in self.contactList:
            print(item)
    def printOnlineList(self):
        for item in self.onlineContacts:
            print(item)


    def __del__(self):
        pass

