#!/usr/bin/env python3
import sys
import ast
import getconf

# construct daemon url

CHAIN = input('Chain:')
RPCURL = getconf.def_credentials(CHAIN)

oraclelist_result = getconf.oracleslist_rpc(CHAIN)

for oracle_txid in oraclelist_result:
    oraclesinfo_result = getconf.oraclesinfo_rpc(CHAIN, oracle_txid)
    description = oraclesinfo_result['description']
    name = oraclesinfo_result['name']
    if description[0:4] == 'CHAT':
        print('[' + name + ': ' + description[5:] + ']: ' + oracle_txid)

    if description[0:5] == 'DCHAT':
        creator_pubkey = description[6:]
        #print('creator_pubkey', creator_pubkey)
        try:
            latest_batons = getconf.get_latest_batontxids(CHAIN, oracle_txid)
            latest_creator_baton = latest_batons[creator_pubkey]
        #print('creatorbaton', latest_creator_baton)
            oraclessamples_result = getconf.oraclessamples_rpc(CHAIN, oracle_txid, latest_creator_baton, 1)
            message_list = ast.literal_eval(oraclessamples_result['samples'][0][0])
            print('[' + name + ': ' + message_list[1] + ']: ' + oracle_txid)
        except:
            continue
