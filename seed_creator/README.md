The `mnemonic.py` module contains methods to generate a mnemonic seed phrase from the 2,048 standard BIP-0039 English words. 
These methods include the ability to generate mnemonic seed phrases based off of a pseudorandom number generator, or the option to generate a repeat mnemonic. A repeat mnemonic is a mnemonic seed phrase of length N whose first N-1 words are the same. The Nth word in the mnemonic seed phrase is determined based off of the a few bits of entropy and a checksum.

For example, if we input the word "zoo" for a 12-word mnemonic seed phrase, one possible repeat mnemonic (out of 128 options) could be
"zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong"

Then we could use other methods in our Mnemonic class to generate private/public keys and addresses to create the following table:


| path              | address                            | public key                                                         | private key                                          |
|-------------------|------------------------------------|--------------------------------------------------------------------|------------------------------------------------------|
| m/44'/160'/0'/0/0 | 2Kx8zKSvMhc5xgcwKTyMGeFcjDhh6x999P | 03cb72ddf5d66e76297c141fd51b3c8c76fed55264f9d1dd939f44c615074fc0b3 | Kx9VZqf8WxZF5Jk9UREqYtjpom7JMNRTxRhYrAgDdDKvSbksjE5Q |
| m/44'/160'/0'/0/1 | 2UTEy5gstc5dyS84PeEGrSQmEJpCgVprhx | 03798b948213263745066690650eeacd2ea6df4d9098e398a87837eb8fa8e0d79a | KwzHf5H7tnSwQqAmjDAF7B6z3bqwuWdTkScD2qrta2BVnoo1uEY6 |
| m/44'/160'/0'/0/2 | 2YJnLwC8FQ4e8ZfrWhjypjfgBYPh2d8iEa | 03e45e928689a032cb0bfad3b5139ea1ec1fb5f3d5769e8aacae31a9b2f1d405e2 | Kzqf8DvaFuK1kWFS5zqbBV1w37bwBpR9sf5hez2tV6pH5PKZWtsX |
| m/44'/160'/0'/0/3 | 2JC6AoKu34JsdwotyuLFzrchF6VNehECP2 | 03d0c9c8c9604fc7231426d27025c3053dd918b6772c5081b28c2f933f7c2580bd | L2PxZofqrZc4PbrNQc4Sr1omqe3pAkkCQndoR1uNGTr8QFpnY6d8 |
| m/44'/160'/0'/0/4 | 2c1wDghUwCLzJUDmpcUfsjCe4cgq6DCMm7 | 02a5c31b073559c77e2483b7496528b6232d09366e797fba6ea93f1df15298afb7 | L2teaXsmCbToRsb5R8yaBG52EggyCqZjvAkoiLi95DjDz4HyHvbB |
| m/44'/160'/0'/0/5 | 2QvccKcamNLMCiNA5ipZpc3f9vWNMwB78g | 029bddcda1b45a58928e70de41bce4603d5ed8abe129bdf4dd84dcad951778c36f | L1M3uzJU8DbFA1RckoWxuANKP9xxWUqDJieevKztqpd6TGC1dcwN |
| m/44'/160'/0'/0/6 | 2cC91mMbbUW3oBzT62tHDZndDAjaAFX17N | 020003d29c9f1cc03f8ded98bbb61ec02979dfa16181faef46f5e05d095c3752bb | L3yQa3Qv3Ev85ubrgaFeBmhxaAjzJEfnpD4PLgTSvm3DJHScwGuJ |
| m/44'/160'/0'/0/7 | 2VTYAQQS8QMicqUBE9zBs4fTDvwYwhmksN | 0244d6bfaca1cb7e9132de80f835ab9a760eaaa37c1f4d5a38e50e2db02859ca7d | L1CYLdu6AfKmsAj32JwgNCLLysv3N4p2eNvpMbc53uqK5m9y5vRt |
| m/44'/160'/0'/0/8 | 2FHDFAwR7vTE7Cf231yQcbYjNJ6emmNcGj | 03672908e972bb001c8d8d94033ded98b37908d64ba058df608221236c73a66885 | L3XqCPUt9PCzP3sadSUanbQ8YoHGMyz1jZkTZD2GW4e1HHnzvADU |
| m/44'/160'/0'/0/9 | 2XJCgTv6idLNjpYRrbaBQmpEfTh2VP5C9i | 02eb66be6eb2491feaba7a4b4e6b68563a715063208e23bdcf3eabf2d924262a9a | L51BwX4pQcTLcooBPLL4RicAr6Yr513EnBta5NXW9L2JCGn4D2YX |
