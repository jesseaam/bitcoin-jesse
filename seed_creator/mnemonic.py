import hashlib
import base58
import hmac
import itertools
import os
import secrets
import unicodedata
from typing import List #, AnyStr, TypeVar, Union

# pseudo-code
# generate 128 bit entropy
# sha256 entropy
# append 1st 4 bits to initial entropy 
# split those 132 bits up by 11 bit list
# convert each 11-bit entry into a word
# create master seed
# generate the 1st 10 priv,pub, and pub-addresses
# search for those address on the block-chain


word = "arrow" # word to repeat in mnemonic code
ms = 24 # mnemonic sentence size
edic = {12: 128, 15:160, 18:192, 21:224, 24:256} # number of bits of entropy given the number of mnemonic code words (see https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
cs_size =  edic[ms] // 32 # checksum
fe = (edic[ms] - (ms - 1)*11)  # number of bits of entropy the last word will encode for)
def free_bits(free_bit_size: int) -> list:
    free = "0" * free_bit_size
    free_list = [free]
    flip = 1
    while flip < 2**free_bit_size:
        free = bin(int(free,2) + 1)[2:].zfill(free_bit_size)
        free_list.append(free)
        flip += 1
    return free_list

freeb = free_bits(fe)
freeb = freeb[0] # just hardcode the possible free bits to 1111111
print(freeb)


# note that this path will need to be modified slightly once it is called from within Flask framework.
d = os.path.join(os.path.dirname(__file__), "wordlist_english.txt")
with open(d, "r", encoding="utf-8") as f:
    wordlist = [w.strip() for w in f.readlines()] # ['abandon', 'ability', ..., "zoo"]

ndx = wordlist.index(word)
ndx = bin(ndx)[2:].zfill(11)
b = ndx * (ms - 1) # entropy in binary
b += freeb # add the extra entropy that the last word encodes for
ent = int(b, 2)
ent = ent.to_bytes(edic[ms]//8, byteorder="big") # convert to bytes
print(ent)

h = hashlib.sha256(ent).hexdigest() #https://bitcoin.stackexchange.com/questions/69957/bip39-manual-phrase-calculations-how-are-multiple-checksums-valid
print(h)
cs = bin(int(h, 16))[2:].zfill(256)[: cs_size]
print(cs)
last_word = freeb + cs
last_word = int(last_word, 2)
last_word = wordlist[last_word]

sentence = (word + " ") * (ms-1)
sentence += last_word
print(sentence)


#def to_bytes(wordlist: List(str), wrd: str) -> bytes:
def to_bytes(wordlist: list(), wrd: str) -> bytes:
    """
    Take as input one word from the mnemonic wordlist. Repeat that word 11 times (hard-coded for now) and convert to bytes.
    """
    ndx = wordlist.index(wrd)
    b = 
    #ndx = bin(ndx)
    ndx = bytes(ndx)
    ndx = int.from_bytes(ndx, byteorder="big")
    print(ndx)
    #ndx = bin(int.from_bytes(ndx, byteorder="big"))[2:]
    return ndx

to_bytes(wordlist=wordlist, wrd="zoo")

someint = 5
bytes_val = someint.to_bytes(2, 'big')

# printing integer in byte representation
print(bytes_val)

import hashlib
#ndx = 2047
#b = bin(ndx)[2:].zfill(11) * 11 # 121 (but don't I need 128?)
b = "10000000000" * 11
print(int("10000000000", 2))
half_ent = "0000001"
b += half_ent # 0000
b = int(b, 2)
b = b.to_bytes(16, byteorder="big")
print(b)
#b = int(b, 2)
#print(b)
#b += b"1111110" # 0011

h = hashlib.sha256(b).hexdigest() #5ac6a5945f16500911219129984ba8b387a06f24fe383ce4e81a73294065461b
# should be https://bitcoin.stackexchange.com/questions/69957/bip39-manual-phrase-calculations-how-are-multiple-checksums-valid
print(h)
cs = bin(int(h, 16))[2:].zfill(256)[: 128 // 32]
cs = half_ent + cs
print(cs)
print(int(cs,2)) # should be 2037 for wrong




# adapted from https://tinyurl.com/trmn172
#def to_mnemonic(self, data: bytes) -> str:
def to_mnemonic(data: bytes) -> str:
        if len(data) not in [16, 20, 24, 28, 32]:
            raise ValueError(
                f"Data length should be one of the following: [16, 20, 24, 28, 32], but it is not {len(data)}."
            )
        h = hashlib.sha256(data).hexdigest()
        b = (
            bin(int.from_bytes(data, byteorder="big"))[2:].zfill(len(data) * 8)
            + bin(int(h, 16))[2:].zfill(256)[: len(data) * 8 // 32]
        )
        result = []
        for i in range(len(b) // 11):
            idx = int(b[i * 11 : (i + 1) * 11], 2)
            #result.append(self.wordlist[idx])
            result.append(wordlist[idx])
        #return self.delimiter.join(result)
        return " ".join(result)

print(to_mnemonic(data=h))


# note that I will go through a for-loop for that first 7 bits of entropy encoded in the final mnemonic word.
# For each of these iterations, I will find the correponding final mnemonic word. I need to figure out why
# I am not getting the appropriate checksum when hashing though. See my comment on this Stack Exchange question:
# https://bitcoin.stackexchange.com/questions/69957/bip39-manual-phrase-calculations-how-are-multiple-checksums-valid
# once I figure that out, I should be able to code everything up.
# * on second thought, I should probably just keep a copy in memory of each of the possible first-7 bits upon instantiation of the class. 


#print(base58.b58encode(b'hello world'))
#print(base58.b58decode(b'StV1DL6CwTryKyV'))
#print(base58.b58encode_check(b'hello world'))


#random_bits = (n_mnemonic * 11) - x*4
#Return a random byte string containing nbytes number of bytes. If nbytes is None or not supplied, a reasonable default is used.
#rdm = secrets.token_bytes(nbytes=(ent // 8)) # ent is in bits
#rdm = int.from_bytes(rdm, byteorder="big")
#print(rdm)
