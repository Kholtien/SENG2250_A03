import random
from otherFunctions import otherFunctions as oF
import hashlib

class RSA:
    def __init__(self):
        self.e = 65537
        self.p = oF.generate_prime_number(1024)
        self.q = oF.generate_prime_number(1024)
        self.n = self.p * self.q               #n or modulus
        self.totient = (self.p - 1) * (self.q - 1)#Totient
        self.d = oF.findModInverse(self.e,self.totient)
        self.publicKey = (self.n,self.e)
        self.privateKey = (self.n,self.d)

def rsaEncrypt(message,e,n):
    return oF.powmod(message,e,n)

def rsaDecrypt(message,d,n):
    return oF.powmod(message,d,n)

def tupleToRsaSignatureAndTuple(tupleToEncrypt,e,n):
    rsaSignatureHash = hashlib.sha256(str(tupleToEncrypt).encode())
    rsaSignatureHashInt = int('0x'+rsaSignatureHash.hexdigest(),16)
    message = [rsaEncrypt(rsaSignatureHashInt,e,n)]
    for part in tupleToEncrypt:
        message.append(part)
    message = tuple(message)

    return message

def rsaBytesToTuple(message):
    messageAsString = message.decode()
    # try:
    #     out = tuple(map(int, messageAsString.replace('(','').replace(')','').split(', ')))
    # else:
    #     out = tuple(messageAsString.replace('(','').replace(')','').split(', '))
    try:
        out = tuple(map(int, messageAsString.replace('(','').replace(')','').split(', ')))
    except:
        out = tuple(messageAsString.replace('(','').replace(')','').split(', '))
    finally:
        return out
    
    
    # return out

def verifySignatureTuple(toVerify,rsaKey):
    encryptedRsaSignature = toVerify[0]
    message = toVerify[1:len(toVerify)]

    rsaSignature = rsaDecrypt(encryptedRsaSignature,int(rsaKey[1]),int(rsaKey[0]))
    rsaSigVerification = int(hashlib.sha256(str(message).encode()).hexdigest(),16)

    if rsaSignature == rsaSigVerification:
        print('Signature Verified')
    else:
        raise Exception("RSA signature does not match. Intruder Alert!")

    return message