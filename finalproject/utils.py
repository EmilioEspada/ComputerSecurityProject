# This files holds all our algorithms and functions required to be used for our notes app
import random
import struct


# Miller-Rabin Primality Test, checks to see if a number is prime
def is_prime(n, k=10):
    if n < 2:
        return False
    if n <= 3:
        return True

    def check(a, d, s):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False

    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    # Repeats primality check several times for accuracy
    for _ in range(k):
        a = random.randrange(2, n - 1)
        if not check(a, d, s):
            return False

    return True


# Generate Prime Number of the specified bit length, uses primality test to ensure prime
def generate_prime(bits):
    while True:
        n = random.randrange(2 ** (bits - 1), 2 ** bits)
        if is_prime(n):
            return n


# Greatest Common Divisor
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# Extended Euclidean Algorithm, used to find modular inverse
def extended_gcd(a, b):
    x, old_x = 0, 1
    y, old_y = 1, 0

    while b != 0:
        quotient = a // b
        a, b = b, a - quotient * b
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y

    return a, old_x, old_y


# Modular Inverse
def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    return x % m


# Generate RSA Keys, public and private pairs
def generate_keys(key_size):
    p = generate_prime(key_size // 2)
    q = generate_prime(key_size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randrange(2 ** (key_size - 1), 2 ** key_size)
        if gcd(e, phi) == 1:
            break

    d = mod_inverse(e, phi)

    public_key = (e, n)
    private_key = (d, n)


    return public_key, private_key


# RSA Encryption of given plaintext using the RSA public key
def encrypt(plaintext, public_key):
    e, n = public_key
    block_size = n.bit_length() // 8  # Determine block size based on key size
    plaintext_blocks = [int.from_bytes(plaintext[i:i + block_size], byteorder='big') for i in
                        range(0, len(plaintext), block_size)]
    ciphertext_blocks = [pow(block, e, n) for block in plaintext_blocks]
    ciphertext = b''.join(block.to_bytes((n.bit_length() + 7) // 8, byteorder='big') for block in ciphertext_blocks)
    return ciphertext


# RSA Decryption of given ciphertext using the RSA private key
def decrypt(ciphertext, private_key):
    d, n = private_key
    block_size = (n.bit_length() + 7) // 8
    ciphertext_blocks = [int.from_bytes(ciphertext[i:i + block_size], byteorder='big') for i in
                         range(0, len(ciphertext), block_size)]
    plaintext_blocks = [pow(block, d, n) for block in ciphertext_blocks]
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
