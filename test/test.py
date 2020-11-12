import sys
sys.path.append('../otherFunctions')

import otherFunctions


e       = 65537
p       = otherFunctions.generate_prime_number(1024)      
q       = otherFunctions.generate_prime_number(1024)      
n       = p * q               
Toitent = (p - 1) * (q - 1)

d       = otherFunctions.findModInverse(e,Toitent)

print(d)

print('done')

print(otherFunctions.powmod(int('hello'.encode()),e,n))