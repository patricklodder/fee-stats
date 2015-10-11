#!/usr/bin/python
# Copyright (c) 2015 Patrick Lodder
#
# Distributed under the MIT software license, see
# http://www.opensource.org/licenses/mit-license.php.
#

from __future__ import print_function
import struct
import sys

from checksigs import *
from blocktools import hashStr
from rpc import BitcoinRPC

settings = {}

def fetch_block(rpc, h, check):
  reply = rpc.execute([rpc.build_request(0, 'getblock', [h, False])]);
  for resp_obj in reply:
      if rpc.response_is_error(resp_obj):
        print('JSON-RPC: error at getblock', file=sys.stderr)
        exit(1)
      hexblock = resp_obj['result']
      block = check(hexblock)
      return hashStr(block.blockHeader.previousHash)

def run(user, passwd, start, num):
  h = None

  rpc = BitcoinRPC('localhost', 22555, user, passwd)
  reply = rpc.execute([rpc.build_request(0, 'getblockhash', [start])]);

  for resp_obj in reply:
      if rpc.response_is_error(resp_obj):
        print('JSON-RPC: error at getblockhash for block ' + start, file=sys.stderr)
        exit(1)
      h = resp_obj['result']

  counter = SigCounter()
  check = lambda b: parseAndCount(counter, b)

  for i in range(0, num):
    h = fetch_block(rpc, h, check)
    if i % 1000 == 999:
      counter.report()

  counter.report()

if __name__ == '__main__':
  if len(sys.argv) != 5:
    print("Usage: linearize-hashes.py RPC_USER RPC_PASS START_BLOCK NUM_BLOCKS")
    sys.exit(1)

  user = sys.argv[1]
  passwd = sys.argv[2]
  start = int(sys.argv[3])
  num = int(sys.argv[4])

  run(user, passwd, start, num)



