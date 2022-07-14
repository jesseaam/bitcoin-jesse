import hashlib
import base58
import hmac
import itertools
import os
import secrets
import unicodedata
#from typing import AnyStr, List, TypeVar, Union

# pseudo-code
# generate 128 bit entropy
# sha256 entropy
# append 1st 4 bits to initial entropy 
# split those 132 bits up by 11 bit list
# convert each 11-bit entry into a word
# create master seed
# generate the 1st 10 priv,pub, and pub-addresses
# search for those address on the block-chain

d = os.path.join(os.path.dirname(__file__), "wordlist_english.txt")
with open(d, "r", encoding="utf-8") as f:
    wordlist = [w.strip() for w in f.readlines()]


#print(base58.b58encode(b'hello world'))
#print(base58.b58decode(b'StV1DL6CwTryKyV'))
#print(base58.b58encode_check(b'hello world'))

# specify how much entropy (see https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
ent = 128 # other possible: 160, 192, 224, or 256 
cs = ent // 32 # checksum
ms = (ent + cs) // 11 # mnemonic sentence
print(ms)

#random_bits = (n_mnemonic * 11) - x*4
#Return a random byte string containing nbytes number of bytes. If nbytes is None or not supplied, a reasonable default is used.
rdm = secrets.token_bytes(nbytes=(ent//8)) # ent is in bits
h = hashlib.sha256(rdm).hexdigest()
print(h)
print(type(h))
