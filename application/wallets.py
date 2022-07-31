from base64 import decode
from seed_creator.mnemonic import Mnemonic
from bip32 import BIP32 # https://github.com/darosior/python-bip32
import hashlib
import json

class Wallet():

    @staticmethod
    def repeat_wallet(repeat_word, mnemonic_size):
        """
        Input
            repeat_word: <class 'str'> A word to repeat in a mnemonic phrase.
            mnemonic_size: <class 'int'> Number of words in the mnemonic phrase. 12,15,18,21,24
        Output
            phrase: <class 'str'> The mnemonic phrase using the repeat_word and mnemonic_size. Note it is hard coded to just manually choose one of multiple possibilites.
            mn_all: <class 'str'> The other possible last words that would work with the repeat_word (note they create different seeds).
            tot: <class 'int'> The number of possible mnemonic phrases using repeat_word.
            funded: <class 'int'> How many sats have been funded to "m/44'/0'/0'/0/0" using the repeat mnemonic to generate the seed. 
            summary: <class 'int'> How many sats are left at the path "m/44'/0'/0'/0/0".
            addr0: <class 'str'> The base58_check encoded address at the path "m/44'/0'/0'/0/0".
            results: <class 'str'> A dictionary turned string containing a summary of: "BIP39 Seed", "BIP32 Root Key", "Master Private Key", "Master Chain Code", "Master Public Key", "Master Public Key Compressed", "Public Keys", and "Addresses".
        """

        mn = Mnemonic()
        mn_all = mn.repeat_mnemonic(repeat_word=repeat_word, mnemonic_size=mnemonic_size)
        tot = len(mn_all)
        phrase = mn_all[0]
        mn_all = [x.split()[-1] for x in mn_all] # just pull last word
        mn_all = mn_all[1:] # all other possible mns (remove the 1 we're showcasing)
        mn_all = " ".join(mn_all)
        seed = mn.to_bip39seed(phrase)
        master_prvkey = mn.master_prv(seed)
        master_cc = mn.master_chain(seed)
        bip32 = BIP32.from_seed(seed)
        root_xprv = bip32.get_xpriv_from_path("m")
        root_xpub = bip32.get_xpub_from_path("m")
        pub, pubc = mn.to_public(master_prvkey)

        # BIP 44: m / purpose' / coin_type' / account' / change / address_index
        bip44_prv = bip32.get_xpriv_from_path("m/44'/0'/0'/0")
        bip44_pub = bip32.get_xpub_from_path("m/44'/0'/0'/0")
        pubkey0 = bip32.get_pubkey_from_path("m/44'/0'/0'/0/0"); addr0 = mn.to_address(pubkey0).decode("ascii")
        pubkey1 = bip32.get_pubkey_from_path("m/44'/0'/0'/0/1"); addr1 = mn.to_address(pubkey1).decode("ascii")

        results = {"BIP39 Seed": seed.hex(),
                "BIP32 Root Key": root_xprv,
                "Master Private Key": master_prvkey.hex(),
                "Master Chain Code": master_cc.hex(),
                "Master Public Key": pub.hex(),
                "Master Public Key Compressed": pubc.hex(),
                "Public Keys": {"m/44'/0'/0'/0/0": pubkey0.hex() ,
                                "m/44'/0'/0'/0/1": pubkey1.hex()},
                "Addresses":   {"m/44'/0'/0'/0/0": addr0,
                                "m/44'/0'/0'/0/1": addr1}
                }

        results = json.dumps(results, indent=2)

        funded, summary = mn.summarize_addr(addr0)
        return (mn_all, phrase, tot, funded, summary, addr0, results)


    @staticmethod
    def random_wallet(mnemonic_size):
        """
        Input
            mnemonic_size: <class 'int'> Number of words in the mnemonic phrase. 12,15,18,21,24
        Output
            phrase: <class 'str'> The mnemonic phrase using the repeat_word and mnemonic_size. Note it is hard coded to just manually choose one of multiple possibilites.
            funded: <class 'int'> How many sats have been funded to "m/44'/0'/0'/0/0" using the repeat mnemonic to generate the seed. 
            summary: <class 'int'> How many sats are left at the path "m/44'/0'/0'/0/0".
            addr0: <class 'str'> The base58_check encoded address at the path "m/44'/0'/0'/0/0".
            results: <class 'str'> A dictionary turned string containing a summary of: "BIP39 Seed", "BIP32 Root Key", "Master Private Key", "Master Chain Code", "Master Public Key", "Master Public Key Compressed", "Public Keys", and "Addresses".
        """

        mn = Mnemonic()
        phrase = mn.generate_random(mnemonic_size=mnemonic_size)
        seed = mn.to_bip39seed(phrase)

        master_prvkey = mn.master_prv(seed)
        master_cc = mn.master_chain(seed)
        bip32 = BIP32.from_seed(seed)
        root_xprv = bip32.get_xpriv_from_path("m")
        root_xpub = bip32.get_xpub_from_path("m")
        pub, pubc = mn.to_public(master_prvkey)

        # BIP 44: m / purpose' / coin_type' / account' / change / address_index
        bip44_prv = bip32.get_xpriv_from_path("m/44'/0'/0'/0")
        bip44_pub = bip32.get_xpub_from_path("m/44'/0'/0'/0")
        pubkey0 = bip32.get_pubkey_from_path("m/44'/0'/0'/0/0"); addr0 = mn.to_address(pubkey0).decode("ascii")
        pubkey1 = bip32.get_pubkey_from_path("m/44'/0'/0'/0/1"); addr1 = mn.to_address(pubkey1).decode("ascii")

        results = {"Mnemonic": phrase,
                "BIP39 Seed": seed.hex(),
                "BIP32 Root Key:": root_xprv,
                "Master Private Key": master_prvkey.hex(),
                "Master Chain Code": master_cc.hex(),
                "Master Public Key": pub.hex(),
                "Master Public Key Compressed": pubc.hex(),
                "Public Keys": {"m/44'/0'/0'/0/0": pubkey0.hex() ,
                                "m/44'/0'/0'/0/1": pubkey1.hex()},
                "Addresses":   {"m/44'/0'/0'/0/0": addr0,
                                "m/44'/0'/0'/0/1": addr1}
                }

        results = json.dumps(results, indent=2)

        funded, summary = mn.summarize_addr(addr0)
        return (phrase, funded, summary, addr0, results)

    
    @staticmethod
    def brain_wallet(phrase:str) -> str:
        """
        Create address from a string phrase.
        https://en.bitcoin.it/wiki/Brainwallet
        """

        phrase = phrase.encode("utf-8")
        prv = hashlib.sha256(phrase).digest()
        pub, _ = Mnemonic.to_public(Mnemonic, privkey=prv)
        addr = Mnemonic.to_address(Mnemonic, pubkey=pub)
        addr = addr.decode("utf-8")
        funded, summary = Mnemonic.summarize_addr(Mnemonic, addr)
        return (addr, funded, summary)