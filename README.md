find high s / low s stats for dogecoin
---

#####Based on code from: 

- [bitcoin/bitcoin](https://hithub.com/bitcoin/bitcoin) (taken from linearize scripts)
- [tenthirtyone/blocktools](https://github.com/tenthirtyone/blocktools) (most simple block parsing code i could find)

##### Added:

- AuxPOW parsing
- p2pkh scriptsig parsing

##### Usage:

To get stats over n blocks, use: `python checkblocks.py RPC_USER RPC_PASS START_BLOCK NUMBLOCKS`, where:

- `RPC_USER` is the value of `rpcuser` in `dogecoin.conf`
- `RPC_PASS` is the value of `rpcpassword` in `dogecoin.conf`
- `START_BLOCK` is the block NUMBER in the active chain to start parsing from
- `NUM_BLOCKS` is the number of blocks to parse, BACKWARDS FROM `START_BLOCK`

To check all signatures in a transaction, use: `python tx.py TX_HEX`, where:

- `TX_HEX` is the entire transaction, serialized as string of hexadecimals (so not the transaction hash)

##### To Do:

- Add p2sh scriptsig parsing
