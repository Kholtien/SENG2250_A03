from random import randrange, getrandbits

# def powmod(base, exponent, modulus):
#     if modulus == 1:
#         return 0
#     t = 1
#     rs = 1
#     while t <= exponent:
#         rs = (rs * base) % modulus
#         t = t + 1
#     return rs

def powmod(base, exponent, modulus) : 
    res = 1     # Initialize result 
  
    # Update x if it is more 
    # than or equal to p 
    base = base % modulus  
      
    if (base == 0) : 
        return 0
  
    while (exponent > 0) : 
          
        # If e is odd, multiply 
        # b with result 
        if ((exponent & 1) == 1) : 
            res = (res * base) % modulus 
  
        # e must be even now 
        exponent = exponent >> 1      # e = e/2 
        base = (base * base) % modulus 
          
    return res

def is_prime(n, k=128):
    """ Test if a number is prime
        Args:
            n -- int -- the number to test
            k -- int -- the number of tests to do
        return True if n is prime
    """
    # Test if n is not even.
    # But care, 2 is prime !
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True
def generate_prime_candidate(length):
    """ Generate an odd integer randomly
        Args:
            length -- int -- the length of the number to generate, in bits
        return a integer
    """
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p
def generate_prime_number(length=1024):
    """ Generate a prime
        Args:
            length -- int -- length of the prime to generate, in          bits
        return a prime
    """
    p = 4
    # keep generating while the primality test fail
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def findModInverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

