from blocktools import *
from block import Block, Tx

def parseAndCount(rpc, counter, hexblock):
	blockstream = bufferize(hexblock, True)
	block = Block(blockstream)
	counter.blocks += 1
	height = -1
	for tx in block.Txs:
		counter.txs += 1
		amountIn = 0
		amountOut = 0
		numIn = 0
		numOut = 0
		numDust = 0

		for vin in tx.inputs:
			if (int(hashStr(vin.prevhash), 16) == 0):
				coinbase = bufferize(vin.scriptSig)
				heightlen = varint(coinbase)
				height = struct.unpack('Q', pad(coinbase.read(heightlen), 8))[0]
				counter.coinbase +=1
				continue
			counter.inputs += 1
			numIn += 1

			txhex = rpc.execute([rpc.build_request(0, 'getrawtransaction', [hashStr(vin.prevhash), False])]);
			itx = Tx(bufferize(txhex[0]['result'], True))

			amountIn += itx.outputs[vin.txOutId].value

		for vout in tx.outputs:
			numOut += 1
			amountOut += vout.value
			if (vout.value < 100000000):
				numDust += 1

		if (amountIn == 0):
			continue

		print "%d,%s,%d,%d,%d,%d,%d,%d,%d" % (height, block.blockHeader.version, tx.size, numDust, numIn, numOut, amountIn, amountOut, amountIn - amountOut)


	return block

class SigCounter:
	def __init__(self):
		self.blocks = 0
		self.txs = 0
		self.coinbase = 0
		self.inputs = 0

	def report(self):
		print "blocks: %d, txs: %d, inputs: %d" % (self.blocks, self.txs, self.inputs)
		#print "cb: %d, low: %d, high: %d, multi: %d, nonder: %d, unknown: %d" % (self.coinbase, self.low, self.high, self.multisig, self.nonDer, self.unknown)

def pad(bytes, target):
	pad = target - len(bytes)
	return bytes+"\0"*pad
