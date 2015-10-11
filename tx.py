import sys

from blocktools import *
from block import Tx, ScriptSig

if __name__ == '__main__':
  if len(sys.argv) != 2:
  	print("Usage: tx.py TX")

  buf = bufferize(sys.argv[1], True)
  tx = Tx(buf)
  for vin in tx.inputs:
  	if (int(hashStr(vin.prevhash), 16) == 0):
  		continue
  	sig = ScriptSig(vin.scriptSig)
  	if not sig.testable:
  		print sig.reason
  	elif sig.lowS:
  		print "LOW S"
  	else:
  		print "HIGH S" 

