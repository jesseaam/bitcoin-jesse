import hashlib
import base58
import hmac
import itertools
import os
import secrets
import unicodedata
#from typing import List , AnyStr, TypeVar, Union


# note that this path will need to be modified slightly once it is called from within Flask framework.
#d = os.path.join(os.path.dirname(__file__), "wordlist_english.txt")
#with open(d, "r", encoding="utf-8") as f:
with open("wordlist_english.txt", "r", encoding="utf-8") as f:
    wordlist = [w.strip() for w in f.readlines()] # ['abandon', 'ability', ..., "zoo"]

word = "arrow" # word to repeat in mnemonic code
ms = 12 # mnemonic sentence size
edic = {12: 128, 15:160, 18:192, 21:224, 24:256} # number of bits of entropy given the number of mnemonic code words (see https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
cs_size =  edic[ms] // 32 # checksum
fe = (edic[ms] - (ms - 1)*11)  # number of bits of entropy the last word will encode for)

def free_bits(free_bit_size: int) -> list[str]:
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
print(freeb)

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
from secp256k1 import PrivateKey, PublicKey # https://pypi.org/project/secp256k1/

# https://learnmeabitcoin.com/technical/mnemonic
mnemonic = "scrap marriage fitness violin squirrel donate end employ purse cargo earth soup"
foo = unicodedata.normalize("NFKD", mnemonic)
mnemonic_bytes = foo.encode("utf-8")

passphrase_bytes = "mnemonic".encode("utf-8")

seed = hashlib.pbkdf2_hmac("sha512", mnemonic_bytes, passphrase_bytes, 2048)
seed = hmac.new(b"Bitcoin seed", seed, digestmod=hashlib.sha512).digest()

seed = int("b8412034956c622deecae16505158e25dc99514535fea1fb6ef0c5f2f707535c1be6f18b550efe5734e91bb7b651079d6b7808e2bc12be3dcb56a5817bc4f9da", 16).to_bytes(length=64, byteorder="big")
print(type(seed))
master_prv = seed[0:32]
print(master_prv.hex())
master_pub = PrivateKey(privkey=master_prv, raw=True).pubkey.serialize(compressed=True) #master_pub = G * master_prv

master_cc = seed[32:]
#print(master_prv)
#print(master_cc)

##############################################################################################################
# BIP32 root key

xprv = b"\x04\x88\xad\xe4"  # Version for private mainnet (4bytes)
#xpub = b"\x04\x88\xb2\x1e"  # Version for private mainnet (4bytes)
xprv += b"\x00" * 9  # Depth (1byte), parent fingerprint (4bytes), and child number(4bytes)
#xpub += b"\x00" * 9  # Depth (1byte), parent fingerprint (4bytes), and child number(4bytes)
xprv += master_cc
#xpub += master_cc
xprv += b"\x00" + master_prv  # add \x00 so prv will be same length as pub
#xpub += master_pub 
# Double hash using SHA256
hashed_xprv = hashlib.sha256(xprv).digest()
hashed_xprv = hashlib.sha256(hashed_xprv).digest()
#hashed_xpub = hashlib.sha256(xpub).digest()
#hashed_xpub = hashlib.sha256(hashed_xpub).digest()

# Append 4 bytes of checksum
xprv += hashed_xprv[:4]
#xpub += hashed_xpub[:4]
print(base58.b58encode(xprv))
#print(base58.b58encode(xpub))




#def pubkey_to_address(pubkey: bytes) -> str:
#    if 'ripemd160' not in hashlib.algorithms_available:
#        raise RuntimeError('missing ripemd160 hash algorithm')
#
#    sha = hashlib.sha256(pubkey).digest()
#    ripe = hashlib.new('ripemd160', sha).digest()


#print(base58.b58encode(xpub))

#seed = '67f93560761e20617de26e0cb84f7234aaf373ed2e66295c3d7397e6d7ebe882ea396d5d293808b0defd7edd2babd4c091ad942e6a9351e6d075a29d4df872af'
#seed = int(seed, 16).to_bytes(64, byteorder="big")
#print(seed)
# Compute HMAC-SHA512 of seed
#seed = hmac.new(b"Bitcoin seed", seed, digestmod=hashlib.sha512).hexdigest()





from secp256k1 import PrivateKey, PublicKey # https://pypi.org/project/secp256k1/
master = '463223aac10fb13f291a1bc76bc26003d98da661cb76df61e750c139826dea8b'
master = int(master, 16).to_bytes(length=32, byteorder="big")
print(master)
#master_prv =  b'\x15|\xd6\x00U\xc6O\xb5h\x9e\xa4\x0e\xd8\xca\x00N1i\xdd\xea\xddX#2\x1d\xbdDhI\x1a\x07\xaa'
master_prv = master
prv = PrivateKey(privkey=master_prv, raw=True)
print(prv)
pub = prv.pubkey.serialize(compressed=False).hex() # prv * G
pub_c = prv.pubkey.serialize(compressed=True).hex() # just the x-coord prefixed with 02 or 03 - if y-coord is even or odd (think finite fields)
# https://bitcoin.stackexchange.com/questions/41662/on-public-keys-compression-why-an-even-or-odd-y-coordinate-corresponds-to-the-p
print(pub, pub_c)
pub = prv.pubkey()



#print(base58.b58encode(b'hello world'))
#print(base58.b58decode(b'StV1DL6CwTryKyV'))
#print(base58.b58encode_check(b'hello world'))


#rdm = secrets.token_bytes(nbytes=(ent // 8)) # ent is in bits
#rdm = int.from_bytes(rdm, byteorder="big")
#print(rdm)
