from Cryptodome.Cipher import AES
import hashlib

def CBCencrypt(plaintext,key,iv):
    numBits = 16
    plainTextList = []
    cipherTextList = []
    iv = int('0x'+hashlib.sha256(str(iv).encode()).hexdigest()[0:4],16)
    for char in plaintext:
        # plainTextList.append(format(ord(char),'#010b')[len(format(ord(char),'#010b')) - 8:])
        plainTextList.append(format(ord(char),'#010b')[len(format(ord(char),'#010b')) - 8:])
    print(plainTextList)
    print(format(iv,'#016b')[len(format(iv,'#016b'))-16:])
    left = iv
    
    for i in range(4):
        right = int('0b'+plainTextList[i*2]+plainTextList[i*2+1],2)
        xor = left ^ right
        print(format(right,'#016b')[len(format(right,'#016b'))-16:],format(left,'#016b')[len(format(left,'#016b'))-16:],format(xor,'#016b')[len(format(xor,'#016b'))-16:],'\n',sep='\n')
        # cipher = AES.new(key,AES.MODE_ECB,nonce=nonce)
        # cipherTextList.append(cipher.encrypt())

    
# def Xor16BitBinary(a,b):


CBCencrypt('abcdefgh',234324,234324)
