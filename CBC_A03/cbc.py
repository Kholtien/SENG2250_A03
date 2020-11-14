from Cryptodome.Cipher import AES
import hashlib
import random

def CBCencrypt(plainText,key,iv):
    """
    Returns a hex string of the cipherText
    """
    numBits = 16
    numBitsW0b = 18
    #below puts the IV through a hash then makes it 128 bits long (16 bytes) and finally changes it to bytes type
    ivAs16Bytes = (int('0x'+hashlib.sha256(str(iv).encode()).hexdigest(),16) % 2**128).to_bytes(16,'big')
    #Turn text into 64 bit binary string
    plainTextAsBits = str(plainText).encode()
    # plainTextAsBits = format(int.from_bytes(plainText.encode(),'big'),'#0514b')
    plainTextAsBitsList = []
    plainTextAs16BitInts = []
    cipherTextList = []

    #break 64 bit binary string into 4 equal parts
    # for i in range(len(plainTextAsBits)//2):
    #     plainTextAsBitsList.append(plainTextAsBits[16*i+2:16*i+18])
    #     plainTextAs16BitInts.append(int('0b'+plainTextAsBitsList[i],2))
    

    # print(plainTextAsBitsList)
    # print(plainTextAsBits)
    # print(plainTextAs16BitInts)

    left = ivAs16Bytes
    outStr = []
    cipher = AES.new(key,AES.MODE_ECB)

    for i in range(len(plainTextAsBits)//16):
        right = plainTextAsBits[i*16:i*16+16]
        preBlockEncrypt = byteXOR(left,right)
        cipherText = cipher.encrypt(preBlockEncrypt)
        #below puts cipherText into a hex format, then adds leading zeros to make it 16 bytes and removes the 0x
        cipherTextList.append(format(int('0x'+cipherText.hex(),16),'#034x')[2:34])
        left = cipherText
    
    out = ''.join(cipherTextList)

    return out

def CBCdecrypt(cipherText,key,iv):
    """
    takes in a hex string and returns a decoded string
    """
    #below puts the IV through a hash then makes it 128 bits long (16 bytes) and finally changes it to bytes type
    ivAs16Bytes = (int('0x'+hashlib.sha256(str(iv).encode()).hexdigest(),16) % 2**128).to_bytes(16,'big')
    cipherTextList = []
    cipher = AES.new(key,AES.MODE_ECB)



    for i in range(len(cipherText)//32):
        cipherTextList.append(cipherText[32*i:32*i+32])
    # print(cipherTextList)

    left = ivAs16Bytes
    outStr = []

    for i in range(len(cipherText)//32):
        cipherTextPartBytes = int('0x' + cipherTextList[i],16).to_bytes(16,'big')

        # cipherTextPartInt = int('0b'+cipherTextList[i],2)
        right = cipher.decrypt(cipherTextPartBytes)
        # right = int.from_bytes(decryptedPart,'big')
        plainTextPart = byteXOR(left,right)
        left = cipherTextPartBytes
        outStr.append(plainTextPart.decode())
    
    return ''.join(outStr)

def byteXOR(b1,b2):
    return bytes(a ^ b for a, b in zip(b1, b2))


def CBCTest():
    iv = random.randrange(2**128)
    key = 101153146228630395303830694709631737433950628137676538287650741735588006718384388996669347164145838162561867995798027180391347274917152763965286860663592510856353735958012961113658933327330290995775717880049638211397218575432070933547824779245933055388430284894534999613188410321834753695155190531750947931967
    k_hash = hashlib.sha256(key.to_bytes(1024,'big'))
    k_ = format(int.from_bytes(k_hash.digest(), 'big'),'#0258b')[2:258]
    k_digest = k_hash.digest()

    message = 'this message is somehow crazily enough exactly sixty four bytes.'
    print(message)
    encryptedMessage = CBCencrypt(message,k_digest,iv)
    print(encryptedMessage)
    decryptedMessage = CBCdecrypt(encryptedMessage,k_digest,iv)
    print(decryptedMessage)


def hmac(k,m):
    """
    k is in bytes from a hash function, m is a string.
    Returns the hmac
    """
    k_len = len(k)
    opad = int('0x'+'5c'*k_len,16).to_bytes(k_len,'big')
    ipad = int('0x'+'36'*k_len,16).to_bytes(k_len,'big')

    kXORipad = byteXOR(k,ipad)
    kXORopad = byteXOR(k,opad)

    return hashlib.sha256(concatBytes(kXORopad,hashlib.sha256(concatBytes(kXORipad,m.encode())).digest())).digest()

def concatBytes(a,b):
    """
    concatnates to byte types together, order matters. this is basically a||b but in bytes
    """
    byteArrayForConcat = bytearray()
    for i in range(len(a)):
        byteArrayForConcat.append(a[i])
    
    for i in range(len(b)):
        byteArrayForConcat.append(b[i])
    
    return bytes(byteArrayForConcat)


def test():
    key = 101153146228630395303830694709631737433950628137676538287650741735588006718384388996669347164145838162561867995798027180391347274917152763965286860663592510856353735958012961113658933327330290995775717880049638211397218575432070933547824779245933055388430284894534999613188410321834753695155190531750947931967
    k_hash = hashlib.sha256(key.to_bytes(1024,'big'))
    k_digest = k_hash.digest()
    message = 'this message is somehow crazily enough exactly sixty four bytes.'

    print('message:',message)
    print('hmac:\t',hmac(k_digest,message))