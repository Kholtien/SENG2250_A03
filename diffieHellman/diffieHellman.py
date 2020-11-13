import random
from otherFunctions import otherFunctions as oF

class DiffieHellman:
    def __init__(self):
        self.prime = int()
        self.generator = int()
        self.privateExp = random.randrange(99999)
        self.key = int()
    
    def calcKeyToShare(self):
        return oF.powmod(self.generator,self.privateExp,self.prime)
    
    def calcSharedPrivate(self,sharedKey):
        return oF.powmod(sharedKey,self.privateExp,self.prime)