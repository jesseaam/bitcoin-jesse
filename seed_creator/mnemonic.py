import hashlib
import base58
import hmac
import itertools
import os
import secrets
import unicodedata
import requests
import json
from secp256k1 import PrivateKey, PublicKey # https://pypi.org/project/secp256k1/



class Mnemonic():
    """This class can be used to generate entropy, convert to an N-word mnemonic, derive
    extended public/private keys, and generate addresses.
    """

    def __init__(self):
        d = os.path.join(os.path.dirname(__file__), "wordlist_english.txt")
        with open(d, "r", encoding="utf-8") as f:
            self.wordlist = [w.strip() for w in f.readlines()] # ["abandon", "ability", ..., "zoo"]

    def generate_random(self, mnemonic_size: int) -> str:
        """Generate a random mnemonic seed phrase given a specific size."""

        edic = {12: 128, 15:160, 18:192, 21:224, 24:256} # number of bits of entropy given the number of mnemonic code words (see https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
        ent = edic[mnemonic_size]
        rdm = secrets.token_bytes(nbytes=(ent // 8)) # ent is in bits
        cs_size =  edic[mnemonic_size] // 32 # checksum
        h = hashlib.sha256(rdm).hexdigest() #https://bitcoin.stackexchange.com/questions/69957/bip39-manual-phrase-calculations-how-are-multiple-checksums-valid
        cs = bin(int(h, 16))[2:].zfill(256)[: cs_size]
        rdm = int.from_bytes(rdm, byteorder="big")
        rdm = f"{rdm:b}".zfill(ent) # convert int to binary string
        combined = rdm + cs

        out_mnemonic = []
        for i in range(mnemonic_size):
            ndx = combined[i*11:(i+1)*11]
            ndx = int(ndx, 2)
            out_mnemonic.append(self.wordlist[ndx])

        return " ".join(out_mnemonic)


    def free_bits(self, free_bit_size: int) -> list[str]:
        """This method is used in conjunction with the repeat_mnemonic method.
        Input the number of bits of entropy the last code-word encodes for.
        Return a list of strings for all possible permutations of that entropy.
        e.g., ["0000000", "0000001", ..., "1111111"]
        """

        free = "0" * free_bit_size
        free_list = [free]
        flip = 1
        while flip < 2**free_bit_size:
            free = bin(int(free,2) + 1)[2:].zfill(free_bit_size)
            free_list.append(free)
            flip += 1
        return free_list


    def repeat_mnemonic(self, repeat_word: str, mnemonic_size: int) -> list:
        """Given a word to repeat in the mnemonic sentence and the number of words
        in the entire mneminc sentence, return what the last word
        (and entire mnemonic sentence) should be to generate the checksum valid.
        Note, last word will have multiple options because of free_bits method.
        e.g.
        Input: "abandon", 12
        Ouput: ["abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
                                                    ...,
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon mouse", "...",
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon wrap"]
        """

        edic = {12: 128, 15:160, 18:192, 21:224, 24:256} # number of bits of entropy given the number of mnemonic code words (see https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
        cs_size =  edic[mnemonic_size] // 32 # checksum
        fe = (edic[mnemonic_size] - (mnemonic_size - 1)*11)  # number of bits of entropy the last word will encode for)
        freeb = self.free_bits(fe)

        ndx = self.wordlist.index(repeat_word)
        ndx = bin(ndx)[2:].zfill(11)
        b = ndx * (mnemonic_size - 1) # entropy in binary

        possible_mnemonics = []
        for i in freeb:
            ent = b + i # add the extra entropy that the last word encodes for
            ent = int(ent, 2)
            ent = ent.to_bytes(edic[mnemonic_size]//8, byteorder="big") # convert to bytes
            h = hashlib.sha256(ent).hexdigest() #https://bitcoin.stackexchange.com/questions/69957/bip39-manual-phrase-calculations-how-are-multiple-checksums-valid
            cs = bin(int(h, 16))[2:].zfill(256)[: cs_size]
            last_word = i + cs
            seed = b + last_word
            last_word = int(last_word, 2)
            last_word = self.wordlist[last_word]
            sentence = ""
            sentence = (repeat_word + " ") * (mnemonic_size-1)
            sentence += last_word
            possible_mnemonics.append(sentence)
        return possible_mnemonics

    def to_bip39seed(self, mnemonic:str, passphrase="mnemonic") -> bytes:
        """Convert a mnemonic phrase into a bip39 seed."""

        norm = unicodedata.normalize("NFKD", mnemonic)
        mnemonic_bytes = norm.encode("utf-8")
        passphrase_bytes = passphrase.encode("utf-8")
        seed = hashlib.pbkdf2_hmac("sha512", mnemonic_bytes, passphrase_bytes, 2048)
        return seed

    # https://github.com/darosior/python-bip32
    # https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#master-key-generation
    def master_prv(self, bip39seed: bytes) -> bytes:
        """Convert bip39 seed to master private key"""

        prv_and_chain = hmac.new(b"Bitcoin seed", bip39seed, digestmod=hashlib.sha512).digest()
        prv = prv_and_chain[0:32]
        return prv

    def master_chain(self, bip39seed: bytes) -> bytes:
        """Convert bip39 seed to master chain code"""

        prv_and_chain = hmac.new(b"Bitcoin seed", bip39seed, digestmod=hashlib.sha512).digest()
        cc = prv_and_chain[32:]
        return cc


    def to_public(self, privkey: bytes) -> bytes:
        """Convert a private key to a public key (both compressed and not)"""

        prv = PrivateKey(privkey=privkey, raw=True)
        pub = prv.pubkey.serialize(compressed=False) # prv * G
        pubc = prv.pubkey.serialize(compressed=True) # prv * G  # just the x-coord prefixed with 02 or 03 - if y-coord is even or odd (think finite fields). also see explaination here: https://bitcoin.stackexchange.com/questions/41662/on-public-keys-compression-why-an-even-or-odd-y-coordinate-corresponds-to-the-p
        return pub, pubc

    def to_address(self, pubkey: bytes) -> bytes:
        """Convert a public key to an P2PKH address"""

        sha = hashlib.sha256()
        rip = hashlib.new('ripemd160')
        sha.update(pubkey)
        rip.update( sha.digest() )
        addr = b'\x00' +  rip.digest()
        cs = hashlib.sha256(hashlib.sha256(addr).digest()).digest()[:4]
        addr += cs
        addr = base58.b58encode(addr)
        return addr

    def summarize_addr(self, addr:str):
        """Use blockstream's API to gather information about a specified address."""

        stats = requests.get(f"https://blockstream.info/api/address/{addr}").text
        stats = json.loads(stats)
        funded = stats["chain_stats"]["funded_txo_sum"]
        spent = stats["chain_stats"]["spent_txo_sum"]
        summary = int(funded) - int(spent)
        return (funded, summary)


    #def to_xprv(self, prv: bytes, cc: bytes) -> bytes:
    #    xprv = b"\x04\x88\xad\xe4"  # Version for private mainnet (4bytes)
    #    xprv += b"\x00" * 9  # Depth (1byte), parent fingerprint (4bytes), and child number(4bytes)
    #    xprv += cc
    #    xprv += b"\x00" + prv  # add \x00 so prv will be same length as pub
    #    ## Double hash using SHA256
    #    hashed_xprv = hashlib.sha256(xprv).digest()
    #    hashed_xprv = hashlib.sha256(hashed_xprv).digest()
    #    ## Append 4 bytes of checksum
    #    xprv += hashed_xprv[:4]
    #    return base58.b58encode(xprv)
