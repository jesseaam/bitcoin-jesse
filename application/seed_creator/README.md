Input 1 word from https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt
Output that word*11 + the checksum word

The goal is to look up the 1st-10th addresses created by that private key.
For example, if we input the word "zoo" the output will be
"zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong"

Then we could output the following information:

```
path,address,public key,private key
m/44'/160'/0'/0/0,2Kx8zKSvMhc5xgcwKTyMGeFcjDhh6x999P,03cb72ddf5d66e76297c141fd51b3c8c76fed55264f9d1dd939f44c615074fc0b3,Kx9VZqf8WxZF5Jk9UREqYtjpom7JMNRTxRhYrAgDdDKvSbksjE5Q
m/44'/160'/0'/0/1,2UTEy5gstc5dyS84PeEGrSQmEJpCgVprhx,03798b948213263745066690650eeacd2ea6df4d9098e398a87837eb8fa8e0d79a,KwzHf5H7tnSwQqAmjDAF7B6z3bqwuWdTkScD2qrta2BVnoo1uEY6
m/44'/160'/0'/0/2,2YJnLwC8FQ4e8ZfrWhjypjfgBYPh2d8iEa,03e45e928689a032cb0bfad3b5139ea1ec1fb5f3d5769e8aacae31a9b2f1d405e2,Kzqf8DvaFuK1kWFS5zqbBV1w37bwBpR9sf5hez2tV6pH5PKZWtsX
m/44'/160'/0'/0/3,2JC6AoKu34JsdwotyuLFzrchF6VNehECP2,03d0c9c8c9604fc7231426d27025c3053dd918b6772c5081b28c2f933f7c2580bd,L2PxZofqrZc4PbrNQc4Sr1omqe3pAkkCQndoR1uNGTr8QFpnY6d8
m/44'/160'/0'/0/4,2c1wDghUwCLzJUDmpcUfsjCe4cgq6DCMm7,02a5c31b073559c77e2483b7496528b6232d09366e797fba6ea93f1df15298afb7,L2teaXsmCbToRsb5R8yaBG52EggyCqZjvAkoiLi95DjDz4HyHvbB
m/44'/160'/0'/0/5,2QvccKcamNLMCiNA5ipZpc3f9vWNMwB78g,029bddcda1b45a58928e70de41bce4603d5ed8abe129bdf4dd84dcad951778c36f,L1M3uzJU8DbFA1RckoWxuANKP9xxWUqDJieevKztqpd6TGC1dcwN
m/44'/160'/0'/0/6,2cC91mMbbUW3oBzT62tHDZndDAjaAFX17N,020003d29c9f1cc03f8ded98bbb61ec02979dfa16181faef46f5e05d095c3752bb,L3yQa3Qv3Ev85ubrgaFeBmhxaAjzJEfnpD4PLgTSvm3DJHScwGuJ
m/44'/160'/0'/0/7,2VTYAQQS8QMicqUBE9zBs4fTDvwYwhmksN,0244d6bfaca1cb7e9132de80f835ab9a760eaaa37c1f4d5a38e50e2db02859ca7d,L1CYLdu6AfKmsAj32JwgNCLLysv3N4p2eNvpMbc53uqK5m9y5vRt
m/44'/160'/0'/0/8,2FHDFAwR7vTE7Cf231yQcbYjNJ6emmNcGj,03672908e972bb001c8d8d94033ded98b37908d64ba058df608221236c73a66885,L3XqCPUt9PCzP3sadSUanbQ8YoHGMyz1jZkTZD2GW4e1HHnzvADU
m/44'/160'/0'/0/9,2XJCgTv6idLNjpYRrbaBQmpEfTh2VP5C9i,02eb66be6eb2491feaba7a4b4e6b68563a715063208e23bdcf3eabf2d924262a9a,L51BwX4pQcTLcooBPLL4RicAr6Yr513EnBta5NXW9L2JCGn4D2YX
m/44'/160'/0'/0/10,2RW4AYFzXftaCsvQsYQtMQERmJr9vNFVRR,02fadd7dbcabe9ee6c3eacd2b9b02159ed1529e2476ae92d7f10cd3a989e493ecc,L5K9xMPvCugeGbkTdRnsZeFcbsqsp15Epaci7b2DehVsdTCLjwHX
m/44'/160'/0'/0/11,2Vfz1J3rjcxM7tKg1zEh26wz9r6QPMHh6e,03dc056a38205a75214da8fbc9bae51474b3738b13dfb06f277e78d5a6316fba4b,KzP3Wg5owZHDWchFkkmmFLgEQMUxrkQyXE9YhTNUf1cJfGp7CYVc
m/44'/160'/0'/0/12,2GGxSoVKtyFZ7dNp66XVhbDQYU66yYHRDk,02778533c7bd7efb87487435768cbe69c3bab3c3efea7baa9a2b90375ef4b01004,KxXH22oPhUSRuUh844TzN3mLbriY4zubqyq9WsFdV1f1sGd2qUkq
m/44'/160'/0'/0/13,2V4Tx68WcTzjVZh4qcvP1xisK47SGHsMXh,0368ecb211b90306da89634524c8495e5d8e089c9094051a744f41dc01042b17fc,L3fzLSGuHibEfc6GMzk1zHirV44FThgHZStPYMqShRS1qss83HN1
m/44'/160'/0'/0/14,2TLUiG3qrRnsbiKW452oLYdBkJvUEWh3DR,032dc733d5d591f1eb7e820ce79562078e9406f33cdd237ec1b26e2022998ad035,KxTTMJ67ed411HeYYiwQyoUW9FZFywrEhikNgSpA5UJ77sEnZyhP
m/44'/160'/0'/0/15,2XBr82gbjKpEb9GBRgHY1c7PX7VnfUNm5Y,032187f5a18d0142f15e5ad8fcd974b455ef2aeab964c16222a055df637b09168e,Kz4UUc2Teb1s9BJpTshhkZcvcKXCBdFTmux9ehoDiiQHKZ5sPBrj
m/44'/160'/0'/0/16,2JwJHwL4oH4TkLNyezRYCfrDi3nZS7SZHZ,0374eb0bdee6e7cccd00ab2cb21c3ca0f05cc47db8eadce37d54f2fed1931dd9ef,KySNAeGRSDZ11SzRziWHQoP7A8kAiX1PZyp53DxHAaeokcKqxTYF
m/44'/160'/0'/0/17,2LEcXKqZVErgzmt415qVikjvHpzgRSHvms,03dad7380376b6b23cad688412d00e4eae8c6e165dfdd5c5eb952b708891643d73,L3kw4uDd4R85g1KgnzZW28UX1ZNzV11esr4i6TXphwp1T2UcFnZ4
m/44'/160'/0'/0/18,2Rn3Yqmq53FiJv7hMD981UqWii1U8e3sfb,02192d3775bdfc94ec6bcf7f0ddeafd87684bfa3f60d4ae61ca381e4985e2f2fdf,Kz5CKnr7obJm7VTZr8HdDBG29vdiBtspJS2zGYntXBN9W7jMGzif
m/44'/160'/0'/0/19,2Fzr1Vk3eTvCw3wZS4o6bmeaTsd3HK4N6Y,02d976f6548d536a4dac96ed5d4749263c55c779f56dffd6775d3ca824ebb6b232,KzAF3vg6CxzH3aqSeMsB76GUwwn9naFn39JbuMDGmxy47vw5tzDi

```