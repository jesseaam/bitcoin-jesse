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

# note that this path will need to be modified slightly once it is called from within Flask framework.
d = os.path.join(os.path.dirname(__file__), "wordlist_english.txt")
with open(d, "r", encoding="utf-8") as f:
    wordlist = [w.strip() for w in f.readlines()] # ['abandon', 'ability', ..., "zoo"]


word = "arrow" # word to repeat in mnemonic code
ms = 12 # mnemonic sentence size
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
freeb = freeb[0] # just hardcode the possible free bits for now

def to_mnemonic(repeat_word: str, mnemonic_size: int, wordlist: list) -> list:
    """
    Given a word to repeat in the mnemonic sentence and the number of words in the entire mneminc sentence, return what the last word (and entire mnemonic sentence) should be to make the checksum valid.
    """
    edic = {12: 128, 15:160, 18:192, 21:224, 24:256} # number of bits of entropy given the number of mnemonic code words (see https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
    cs_size =  edic[mnemonic_size] // 32 # checksum
    fe = (edic[ms] - (ms - 1)*11)  # number of bits of entropy the last word will encode for)
    freeb = free_bits(fe) #just select one for now

    ndx = wordlist.index(word)
    ndx = bin(ndx)[2:].zfill(11)
    b = ndx * (ms - 1) # entropy in binary

    possible_mnemonics = []
    for i in freeb:
        ent = b + i # add the extra entropy that the last word encodes for
        ent = int(ent, 2)
        ent = ent.to_bytes(edic[ms]//8, byteorder="big") # convert to bytes
        h = hashlib.sha256(ent).hexdigest() #https://bitcoin.stackexchange.com/questions/69957/bip39-manual-phrase-calculations-how-are-multiple-checksums-valid
        cs = bin(int(h, 16))[2:].zfill(256)[: cs_size]
        last_word = i + cs
        seed = b + last_word
        last_word = int(last_word, 2)
        last_word = wordlist[last_word]
        sentence = ""
        sentence = (word + " ") * (ms-1)
        sentence += last_word
        possible_mnemonics.append(sentence)
    return possible_mnemonics

all = to_mnemonic(word, 12, wordlist)
print(all[0])


seed = "0000110010100001100101000011001010000110010100001100101000011001010000110010100001100101000011001010000110010100001100101000000000000000111"
seed = int(seed, 2)
print(seed)

seed.to_bytes(byteorder="big") # convert to bytes


def normalize_string(txt: AnyStr) -> str:
    if isinstance(txt, bytes):
        utxt = txt.decode("utf8")
    elif isinstance(txt, str):
        utxt = txt
    else:
        raise TypeError("String value expected")

    return unicodedata.normalize("NFKD", utxt)



#https://docs.python.org/3/library/unicodedata.html
# Return the normal form form for the Unicode string unistr. Valid values for form are ‘NFC’, ‘NFKC’, ‘NFD’, and ‘NFKD’.
# Two seemingly matching characters that don’t match.
#The answer  is Unicode normalization
import hashlib
import unicodedata
import base58
import hmac
foo = unicodedata.normalize("NFKD", "hello")
mnemonic_bytes = foo.encode("utf-8")
passphrase_bytes = "mnemonic".encode("utf-8")

stretched = hashlib.pbkdf2_hmac("sha512", mnemonic_bytes, passphrase_bytes, 2048)
stretched = stretched[:64]
seed = hmac.new(b"Bitcoin seed", stretched, digestmod=hashlib.sha512).digest()

xprv = b"\x04\x88\xad\xe4"  # Version for private mainnet
xprv += b"\x00" * 9  # Depth, parent fingerprint, and child number
xprv += seed[32:]  # Chain code
xprv += b"\x00" + seed[:32]  # Master key
# Double hash using SHA256
hashed_xprv = hashlib.sha256(xprv).digest()
hashed_xprv = hashlib.sha256(hashed_xprv).digest()

# Append 4 bytes of checksum
xprv += hashed_xprv[:4]
print(xprv)

print(base58.b58encode(xprv))



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
