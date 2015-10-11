# BSD-3 License
# Copyright 2015 - Alex Gorale
# Copyright 2015 - Patrick Lodder

from blocktools import *

MAX_S = int("7fffffffffffffffffffffffffffffff5d576e7357a4501ddfe92f46681b20a0", 16)

class BlockHeader:
	def __init__(self, blockchain, parseAux=True):
		self.version = uint4(blockchain)
		self.previousHash = hash32(blockchain)
		self.merkleHash = hash32(blockchain)
		self.time = uint4(blockchain)
		self.bits = uint4(blockchain)
		self.nonce = uint4(blockchain)
		self.auxpow = None 
		if parseAux and (self.version & 0x620100 == 0x620100):
			self.auxpow = AuxPow(blockchain)
			
			#self.parentHeader = BlockHeader(blockchain)
	def toString(self):
		print "Version:\t 0x%02x" % self.version
		print "Previous Hash\t %s" % hashStr(self.previousHash)
		print "Merkle Root\t %s" % hashStr(self.merkleHash)
		print "Time\t\t 0x%02x" % self.time
		print "Difficulty\t 0x%08x" % self.bits
		print "Nonce\t\t %s" % self.nonce
		if self.auxpow:
			self.auxpow.toString();

class AuxPow:
	def __init__(self, blockchain):
		self.auxCbMerkle = []
		self.auxBlockMerkle = []
		
		self.auxCoinBase = Tx(blockchain)
		self.auxPow = hash32(blockchain)

		self.auxCbMerkleNum = varint(blockchain)
		for i in range(0, self.auxCbMerkleNum):
			self.auxCbMerkle.append(hash32(blockchain))

		self.whatsThis = uint4(blockchain)

		self.auxBlockMerkleNum = varint(blockchain)
		for i in range(0, self.auxBlockMerkleNum):
			self.auxBlockMerkle.append(hash32(blockchain))

		self.auxChainIndex = uint4(blockchain)
		self.auxHeader = BlockHeader(blockchain, False)

	def toString(self):
		print self

class Block:
	def __init__(self, blockchain):
		self.setHeader(blockchain)
		self.txCount = varint(blockchain)
		self.Txs = []

		for i in range(0, self.txCount):
			tx = Tx(blockchain)
			self.Txs.append(tx)

	def setHeader(self, blockchain):
		self.blockHeader = BlockHeader(blockchain)

	def toString(self):
		print "#"*10 + " Block Header " + "#"*10
		self.blockHeader.toString()
		print 
		print "##### Tx Count: %d" % self.txCount
		for t in self.Txs:
			t.toString()

class Tx:
	def __init__(self, blockchain):
		self.version = uint4(blockchain)
		self.inCount = varint(blockchain)
		self.inputs = []
		for i in range(0, self.inCount):
			input = txInput(blockchain)
			self.inputs.append(input)
		self.outCount = varint(blockchain)
		self.outputs = []
		if self.outCount > 0:
			for i in range(0, self.outCount):
				output = txOutput(blockchain)
				self.outputs.append(output)	
		self.lockTime = uint4(blockchain)
		
	def toString(self):
		print ""
		print "="*10 + " New Transaction " + "="*10
		print "Tx Version:\t 0x%02x" % self.version
		print "Inputs:\t\t %d" % self.inCount
		for i in self.inputs:
			i.toString()

		print "Outputs:\t %d" % self.outCount
		for o in self.outputs:
			o.toString()
		print "Lock Time:\t %d" % self.lockTime
				

class txInput:
	def __init__(self, blockchain):
		self.prevhash = hash32(blockchain)
		self.txOutId = uint4(blockchain)
		self.scriptLen = varint(blockchain)
		self.scriptSig = blockchain.read(self.scriptLen)
		self.seqNo = uint4(blockchain)

	def toString(self):
		print "Previous Hash:\t %s" % hashStr(self.prevhash)
		print "Tx Out Index:\t %8x" % self.txOutId
		print "Script Length:\t %d" % self.scriptLen
		print "Script Sig:\t %s" % hashStr(self.scriptSig)
		print "Sequence:\t %8x" % self.seqNo
		
class txOutput:
	def __init__(self, blockchain):	
		self.value = uint8(blockchain)
		self.scriptLen = varint(blockchain)
		self.pubkey = blockchain.read(self.scriptLen)

	def toString(self):
		print "Value:\t\t %d" % self.value
		print "Script Len:\t %d" % self.scriptLen
		print "Pubkey:\t\t %s" % hashStr(self.pubkey)

class ScriptSig:
	def __init__(self, instr):
		buf = bufferize(instr)
		self.testable = False
		self.reason = "unknown"
		self.lowS = False
		self.size = uint1(buf)
		if self.size != 0x00:
			self.der = uint1(buf)
			if self.der == 0x30:
				self.totalSigSize = uint1(buf)
				if uint1(buf) == 0x02:
					self.rSize = uint1(buf)
					self.r = buf.read(self.rSize)
					if uint1(buf) == 0x02:
						self.testable = True
						self.sSize = uint1(buf)
						self.s = buf.read(self.sSize)
						self.lowS = (int(hashStr(self.s), 16) < MAX_S)
			else:
				self.reason = "non-DER"
		else:
			self.reason = "multisig"




