import random

# Generates and returns the public/private keys as a tuple (n, e, d). Prime numbers p and
# needed to generate the keys are picked from the interval [lo, hi).
# Returns a list of primes from the interval [lo, hi).
def _primes(lo, hi):
    list_p = []
    n = lo

    for i in range(lo, hi):
        if isprime(n):
            list_p.append(n)
            n += 1
        else:
            n += 1

    return list_p  # Take this (L)ist


def isprime(n):
    """_summary_

    Args:
        n (_type_): _description_

    Returns:
        _type_: _description_
    """
    if n <= 2:
        return False

    for i in range(2, n - 2):
        if n % i == 0:
            return False
    return True


def keygen(hi, lo=50):
    """
    Returns the public key (n, e) and private key (n, d) as a tuple (n, e, d).
    
    Args:
        hi (int): Upper end of range from which to generate keys .
        lo (int, optional): Lower end of range from which to generate keys. Default is 0.

    Returns:
        tuple: (n, e, d).
    """
    rp_list = _primes(lo, hi)

    while True:
        p = (_sample(rp_list, len(rp_list)))
        p = p[random.randint(0, len(p)-1)]
        q = (_sample(rp_list, len(rp_list)))
        q = q[random.randint(0, len(q)-1)]

        if p != q:
            break

    m = (p - 1)*(q - 1)
    n = p * q
    rp_list2 = _primes(2, m)

    while True:
        e = rp_list2[random.randint(0, len(rp_list2)-1)]
        d = rp_list2[random.randint(0, len(rp_list2)-1)]

        if m % e != 0 and (e * d) % m == 1 and 1 < d < m:
            break

    return n, e, d


# Encrypts x (int) using the public key (n, e) and returns the encrypted value.
def encrypt(x, n, e):
    return (x ** e) % n


# Decrypts y (int) using the private key (n, d) and returns the decrypted value.
def decrypt(y, n, d):
    return (y ** d) % n


# Returns the least number of bits needed to represent n.
def bitLength(n):
    return len(bin(n)) - 2


# Returns the binary representation of n expressed in decimal, having the given width, and padded
# with leading zeros.
def dec2bin(n, width):
    return format(n, '0%db' % width)


# Returns the decimal representation of n expressed in binary.
def bin2dec(n):
    return int(n, 2)


# Returns a list containing a random sample (without replacement) of k length from the list a.
def _sample(prime_list, length):
    b = [prime_list[x] for x in range(0, len(prime_list))]

    for i in range(length):
        x = random.randint(0, len(prime_list)-1)
        hold = b[x]
        b[x] = b[i]
        b[i] = hold

    return b[:length]


# Returns a random item from the list a.
def _choice(a):
    r = random.randrange(0, len(a))
    return a[r]


# Unit tests the library.
def _main():
    x = 18  # example
    n, e, d = keygen(25, 100)
    encrypted = encrypt(x, n, e)
    print(f'encrypt({x}) = {encrypted}\n')
    decrypted = decrypt(encrypted, n, d)
    print(f'decrypt({encrypted}) = {decrypted}\n')
    width = bitLength(x)
    print(f'bitLength({x}) = {width}\n')
    xBinary = dec2bin(x, width)
    print(f'dec2bin({x}) = {xBinary}\n')
    print(f'bin2dec({xBinary}) = {bin2dec(xBinary)}\n')


if __name__ == '__main__':
    _main()
    