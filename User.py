import json

class User:
    def __init__(self):
        #note this will need to first decrypt file when it is enrypted
        myFile = open("information.json")
        jsonFile = json.load(myFile)
        myFile.close()

        self.name = jsonFile["user"][0]["name"]
        self.salt = jsonFile["user"][0]["salt"]
        self.email = jsonFile["user"][0]["email"]
        self.passHash = jsonFile["user"][0]["password"]

    def __del__(self):
        pass
        