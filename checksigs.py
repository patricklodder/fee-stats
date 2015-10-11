from blocktools import *
from block import Block, ScriptSig

def parseAndCount(counter, hexblock):
	blockstream = bufferize(hexblock, True)
	block = Block(blockstream)
	counter.blocks += 1
	for tx in block.Txs:
		counter.txs += 1
		for vin in tx.inputs:
			if (int(hashStr(vin.prevhash), 16) == 0):
				counter.coinbase +=1
				continue
			counter.sigs += 1
			sig = ScriptSig(vin.scriptSig)
			if sig.testable:
				if sig.lowS: 
					counter.low += 1
				else:
					counter.high +=1
			else:
				if sig.reason == "multisig":
					counter.multisig += 1
				elif sig.reason == "non-DER":
					counter.nonDer += 1
				else:
					counter.unknown += 1
	return block

class SigCounter:
	def __init__(self):
		self.blocks = 0
		self.txs = 0
		self.coinbase = 0
		self.sigs = 0
		self.low = 0
		self.high = 0
		self.multisig = 0
		self.nonDer = 0
		self.unknown = 0
	def report(self):
		print "blocks: %d, txs: %d, sigs: %d" % (self.blocks, self.txs, self.sigs)
		print "cb: %d, low: %d, high: %d, multi: %d, nonder: %d, unknown: %d" % (self.coinbase, self.low, self.high, self.multisig, self.nonDer, self.unknown)

