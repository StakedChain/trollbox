#!/usr/bin/env python3
import sys
import codecs
import subprocess
import requests
import json
import time
import getconf

ORCLID = sys.argv[2]
CHAIN = sys.argv[1]

# construct daemon url
RPCURL = getconf.def_credentials(CHAIN)

while True:
    message = "{\"t\": " + str(int(time.time())) + ", \"m\": \"" + input("Type message: ") + "\"}"


    #convert message to hex
    rawhex = codecs.encode(message).hex()

    #get length in bytes of hex in decimal
    bytelen = int(len(rawhex) / int(2))
    hexlen = format(bytelen, 'x')

    #get length in big endian hex
    if bytelen < 16:
        bigend = "000" + str(hexlen)
    elif bytelen < 256:
        bigend = "00" + str(hexlen)
    elif bytelen < 4096:
        bigend = "0" + str(hexlen)
    elif bytelen < 65536:
        bigend = str(hexlen)
    else:
        print("message too large, must be less than 65536 characters")
        continue

    #convert big endian length to little endian, append rawhex to little endian length
    lilend = bigend[2] + bigend[3] + bigend[0] + bigend[1]
    fullhex = lilend + rawhex

    orclpayload = {
        "jsonrpc": "1.0",
        "id": "python",
        "method": "oraclesdata",
        "params": [ORCLID, fullhex]}

    # make oraclesdata rpc call, assign result to rawtx
    call_result = getconf.post_rpc(RPCURL, orclpayload)
    rawtx = call_result['result']['hex']
    
    sendrawpayload = {
        "jsonrpc": "1.0",
        "id": "python",
        "method": "sendrawtransaction",
        "params": [rawtx]}
    #send raw tx
    getconf.post_rpc(RPCURL, sendrawpayload)
