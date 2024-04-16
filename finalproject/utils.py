# This files holds all our algorithms and functions required to be used for our notes app -Emilio Espada
import random
import struct


# This function implements the Miller-Rabin primality test, which is a probabilistic algorithm to determine if a
# given number n is prime. It uses the helper function check(a, d, s) to perform the actual test. The outer loop
# repeats the test k times (default is 10) with different random bases a for increased accuracy. The function returns
# True if n is likely prime, and False otherwise.
def is_prime(n, k=10):
    # If the input number is less than 2, it's not prime
    if n < 2:
        return False
    # 2 and 3 are prime numbers, so return True for these cases
    if n <= 3:
        return True

    # Helper function for performing the Miller-Rabin primality check
    def check(a, d, s):
        # Calculate x = a^d mod n
        x = pow(a, d, n)
        # If x is 1 or n-1, it's a strong pseudo-prime
        if x == 1 or x == n - 1:
            return True
        # Perform s-1 iterations of the squaring step
        for _ in range(s - 1):
            x = pow(x, 2, n)
            # If x becomes n-1, it's a strong pseudo-prime
            if x == n - 1:
                return True
        # If none of the conditions are met, it's a composite number
        return False

    # Calculate d and s for the given number
    # d is the largest odd factor of n-1
    # s is the number of times n-1 is divisible by 2
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    # Repeats the primality check several times for accuracy
    for _ in range(k):
        # Choose a random base a in the range [2, n-2]
        a = random.randrange(2, n - 1)
        # If check(a, d, s) returns False, n is composite
        if not check(a, d, s):
            return False

    # If all iterations pass, n is considered prime
    return True


# This function generates a random prime number of the specified bit length. It repeatedly generates random numbers
# within the desired bit range and checks if they are prime using the is_prime function. Once a prime number is
# found, it is returned.
def generate_prime(bits):
    # Keep generating random numbers until a prime is found
    while True:
        # Generate a random number in the desired bit range
        n = random.randrange(2 ** (bits - 1), 2 ** bits)
        # Check if n is prime using the Miller-Rabin test
        if is_prime(n):
            return n


#  This function calculates the greatest common divisor (GCD) of two integers a and b using the Euclidean algorithm.
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# This function implements the extended Euclidean algorithm, which not only finds the GCD of a and b,
# but also calculates the modular inverses of a modulo b and b modulo a. These modular inverses are used in the RSA
# decryption process.
def extended_gcd(a, b):
    # Initialize variables for the extended Euclidean algorithm
    x, old_x = 0, 1
    y, old_y = 1, 0

    # Perform the extended Euclidean algorithm
    while b != 0:
        quotient = a // b
        a, b = b, a - quotient * b
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y

    # Return the GCD, modular inverse of a modulo b, and modular inverse of b modulo a
    return a, old_x, old_y


# This function calculates the modular inverse of a modulo m using the extended_gcd function. If the GCD of a and m
# is not 1, it means that the modular inverse does not exist, and the function raises a ValueError. Otherwise,
# it returns the modular inverse of a modulo m, which is calculated as x % m, where x is the value returned by the
# extended_gcd function.
def mod_inverse(a, m):
    # Use the extended Euclidean algorithm to find the modular inverse
    g, x, y = extended_gcd(a, m)
    # If the GCD is not 1, the modular inverse doesn't exist
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    # Return the modular inverse of a modulo m
    return x % m


# This function generates a pair of public and private keys for the RSA crypto system. It first generates two
# distinct prime numbers p and q using the generate_prime function. It then calculates n as the product of p and q,
# and phi(n) (the totient function) as (p-1)*(q-1). The public exponent e is chosen as a random number coprime to
# phi(n). The private exponent d is calculated as the modular inverse of e modulo phi(n) using the mod_inverse
# function. Finally, the function returns the public key (e, n) and the private key (d, n).
def generate_keys(key_size):
    # Generate two distinct prime numbers of key_size//2 bits
    p = generate_prime(key_size // 2)
    q = generate_prime(key_size // 2)
    # Calculate n as the product of p and q
    n = p * q
    # Calculate phi(n) as (p-1)*(q-1)
    phi = (p - 1) * (q - 1)

    # Choose a public exponent e that is coprime with phi(n)
    while True:
        e = random.randrange(2 ** (key_size - 1), 2 ** key_size)
        if gcd(e, phi) == 1:
            break

    # Calculate the private exponent d as the modular inverse of e modulo phi(n)
    d = mod_inverse(e, phi)

    # Construct the public and private key pairs
    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key


# This function encrypts the given plaintext using the RSA public key (e, n). It first divides the plaintext into
# blocks of size determined by the key size. Each plaintext block is then raised to the power of the public exponent
# e modulo n, producing a ciphertext block. The final ciphertext is constructed by joining all the ciphertext blocks.
def encrypt(plaintext, public_key):
    # Unpack the public key components
    e, n = public_key
    # Determine the block size based on the key size
    block_size = n.bit_length() // 8
    # Split the plaintext into blocks of the appropriate size
    plaintext_blocks = [int.from_bytes(plaintext[i:i + block_size], byteorder='big') for i in
                        range(0, len(plaintext), block_size)]
    # Encrypt each plaintext block using the public key
    ciphertext_blocks = [pow(block, e, n) for block in plaintext_blocks]
    # Construct the ciphertext by joining the encrypted blocks
    ciphertext = b''.join(block.to_bytes((n.bit_length() + 7) // 8, byteorder='big') for block in ciphertext_blocks)
    return ciphertext


# This function decrypts the given ciphertext using the RSA private key (d, n). It first divides the ciphertext into
# blocks of size determined by the key size. Each ciphertext block is then raised to the power of the private
# exponent d modulo n, producing a plaintext block. The final plaintext is constructed by joining all the blocks.
def decrypt(ciphertext, private_key):
    # Unpack the private key components
    d, n = private_key
    # Determine the block size based on the key size
    block_size = (n.bit_length() + 7) // 8
    # Split the ciphertext into blocks of the appropriate size
    ciphertext_blocks = [int.from_bytes(ciphertext[i:i + block_size], byteorder='big') for i in
                         range(0, len(ciphertext), block_size)]
    # Decrypt each ciphertext block using the private key
    plaintext_blocks = [pow(block, d, n) for block in ciphertext_blocks]
    # Construct the plaintext by joining the decrypted blocks
    plaintext = b''.join(block.to_bytes(block_size, byteorder='big') for block in plaintext_blocks)
    return plaintext


# Tested Tiger hash outside of project, still have to implement within project
# Tiger hash constants
tiger_constants = [
    0x8ba25628474e14c9, 0xe9f84EE8b9b54d57, 0x0D14D4B2747AF248, 0x12D9810213B2915C,
    0x7B6c4708be95df3c, 0x7d2914f49b7574bc, 0x709034953e1d9806, 0x2b60affdea195ffb
]

# Tiger hash initialization values
tiger_init = [
    0x0123456789ABCDEF, 0xFEDCBA9876543210, 0xF096A5B4C3B2E187, 0x07D36F5C8B862300
]

# Tiger hash round functions
t1 = lambda x: (x & 0xFFFFFFFF) ^ ((x >> 32) & 0xFFFFFFFF)
t2 = lambda x: (x & 0x7FFFFFFF) ^ ((x >> 31) & 0x7FFFFFFF) ^ ((x >> 32) & 0x7FFFFFFF)
t3 = lambda x: (x & 0x1FFFFFFF) ^ ((x >> 29) & 0x1FFFFFFF) ^ ((x >> 30) & 0x1FFFFFFF) ^ ((x >> 31) & 0x1FFFFFFF)
t4 = lambda x: (x & 0x0FFFFFFF) ^ ((x >> 27) & 0x0FFFFFFF) ^ ((x >> 28) & 0x0FFFFFFF) ^ ((x >> 29) & 0x0FFFFFFF) ^ (
        (x >> 30) & 0x0FFFFFFF)


# Tiger compression function
def tiger_compress(data, state):
    values = [0] * 8
    values[:4] = state[:4]

    for i in range(8):
        chunk = data[i * 8:(i + 1) * 8]
        chunk += b'\x00' * (8 - len(chunk))  # Padding to ensure exactly 8 bytes
        values[i % 4] ^= struct.unpack(">Q", chunk)[0]

    for i in range(8):
        x = t1(values[0] - (values[7] ^ tiger_constants[i % 8])) ^ values[4]
        y = t2(values[2] + tiger_constants[(i + 4) % 8])
        z = t3(values[1] + (values[3] ^ y))
        values[3] = (values[3] ^ x)
        values[1] = values[2]
        values[2] = values[1] ^ y ^ z
        values[0] = y
        values = values[1:] + values[:1]
        values[4:8] = [values[4] ^ x, values[5] ^ y, values[6] ^ z, values[7] ^ (x ^ y ^ z)]

    state[:4] = [state[i] ^ values[i % 4] for i in range(4)]
    return state


# Tiger hash function
def tiger_hash(data):
    state = list(tiger_init)
    length = len(data) * 8
    data += b'\x01'
    data += b'\x00' * ((7 - len(data) % 8) % 8)
    for i in range(0, len(data), 8):
        state = tiger_compress(data[i:i + 8], state)

    length_bits = length.to_bytes(8, byteorder='little')
    for i in range(8):
        state = tiger_compress(length_bits[i::8], state)

    return ''.join([format(state[i], '016x') for i in range(4)])

# message = b"The quick brown fox jumps over the lazy dog"
# print(tiger_hash(message))
