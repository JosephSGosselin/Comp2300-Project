from Crypto.PublicKey import RSA
from utils import get_random_string
def genRSAKeys ():
    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    file_out = open("public.pem", "wb")
    file_out.write(public_key)
    file_out.close()

def getPubKey ():
    recipient_key = RSA.import_key(open("public.pem").read())
    return str(recipient_key.export_key())



