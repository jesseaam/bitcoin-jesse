# bitcoin-jesse

**Ideas**
- [ ] Create an issue for each of the following and then resolve them with a commit.
- [ ] create links to helpful resources (e.g., learnmeabitcoin, https://allprivatekeys.com/mnemonic-code-converter#english, Saylor series: what is money, dergigi message to friends and family, Mastering Bitcoin)
- [ ] create a function that will calculate what the 12th mnemonic word should be if you chose the first 11-words to be the same. E.g., zoo, zoo, ..., zoo, wrong. Do this for all ~2000 words. Note that there will be 64 solutions for each 11-word set since the last word encodes 7 bits of randomness plut the 4 bit checksum.
- [ ] create a database of the lookups. This should include the number of txs and the current amount held in each address. 
- [ ] Describe how public/private key pairs are created. Use Jupyter notebook to show examples of how seed is created.
- [ ] Talk about the Elliptic curve secp256k1 is used and the parameters. Break out my old abstract algebra book to talk about the definition of a finite field.
- [ ] Talk about running a local version of bitcoin wit regtest ([regression test mode](https://bitcoin.stackexchange.com/questions/109653/why-is-regtest-called-regtest)). Have links to Saylor.edu and https://bitcoindev.network/bitcoin-cli-sandbox/  show how addresses are made and how hdkeypath changes for each address. 
- [ ] Create secure login
- [X] Add current price
