from csv import DictWriter
import json
from unittest import async_case
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import sys
from pybp.pederson import PedersonCommitment
from pybp.rangeproof import RangeProof
from fastapi.responses import  FileResponse
import pickle
import zipfile
import os
import time
import asyncio
from web3 import Web3 
from app.Zokrates_prover import *



web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
 
abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_value",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_hx",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_hy",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_b",
				"type": "uint256"
			}
		],
		"name": "openBid",
		"outputs": [
			{
				"internalType": "string",
				"name": "res",
				"type": "string"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "ap_x",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "ap_y",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "sp_x",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "sp_y",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "t1p_x",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "t1p_y",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "t2p_x",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "t2p_y",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "tau",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "mu",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "t",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "pff",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "rp_x",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "rp_y",
						"type": "uint256"
					}
				],
				"internalType": "struct Open.Proof",
				"name": "pf",
				"type": "tuple"
			}
		],
		"name": "receiveProof",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "s1",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "s2",
				"type": "string"
			}
		],
		"name": "compareStringsbyBytes",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "pure",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "retrieveBid",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "value",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "hx",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "hy",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "b",
						"type": "uint256"
					}
				],
				"internalType": "struct Open.Bidder[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "myname",
				"type": "string"
			}
		],
		"name": "retrieveProof",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "ap_x",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "ap_y",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "sp_x",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "sp_y",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "t1p_x",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "t1p_y",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "t2p_x",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "t2p_y",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "tau",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "mu",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "t",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "pff",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "rp_x",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "rp_y",
						"type": "uint256"
					}
				],
				"internalType": "struct Open.Proof",
				"name": "pf",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"  
	}
]
contract = web3.eth.contract(address='0xD6c5AfCf3c48D5718be0A3B50E42d9ad420ebDa4', abi=abi) 
address = '0xD656fAd2D330bC98f2Fd7D990463397aA81953a2'
priv_key = 'fed3000ead31e8bc837793a406e2f65ea076dd5b224769fa967a854f670bc186'

app = FastAPI()  
  
origins = [
    "http://localhost:3000",    
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
bids = []
price = {}
close = "0"

@app.post("/bid", tags=["bids"])  
async def add_bids(bid: dict) -> str:
    '''
    add bid. format receive id, bid_x, bid_y (pedersen commitment is applied)
    
    '''
    if close == "0":
        bids.append(bid)  
        return "0"
    else:
        return str(close)


@app.get("/close", tags=["closing"])    
async def close_bids() -> str:
    global close
    close = "1"
    return "Not accept anymore"  

checking = 0

stored = {}

@app.get("/bfcheck")
async def bf_check()->str:
    global close
    if close =="0":
        return "Not closed anymore"
    if len(bids) ==0:
        return "Nothing in bids"
    else:
        return "Please enter your value"  
 
verf = 0   
def verf_stored():
    global verf
    global stored
    if verf == 1:
        return
    else:
        verf = 1
        arr = contract.functions.retrieveBid().call()
        for item in arr:
            stored[item[0]] = PedersonCommitment(item[1], b=item[4], h=(item[2],item[3])).get_commitment()
            price[item[0]] = item[1]

@app.post("/check")
async def check_bids(pcval:dict) -> str: 
    '''
    receive r, h, value and check that bidders don't lie 
    '''
    verf_stored()

    computedPC = 0
    for bid in bids:
        if bid['id'] == pcval['id']:
            
            
            computedPC =stored[bid['id']]
            if int(bid['bid_x']) == computedPC[0] and int(bid['bid_y']) == computedPC[1]:
                return "Confirmed"
            else:
                bids.remove(bid)    
                return "You are not allowed to participate"  

verf_check = 0 
@app.post("/get_win") 
async def get_winner(id:dict):
    '''
    if winning bid, notify you are the winner. if losing bid, send proof to verify that you are not winner 
    '''
    win_bid = max(price.values())  
    for idx in price:
        if price[idx] == win_bid:
            win_idx = idx
            break  
    
    if win_idx == id['id']:
        return "You are the winner"
    
    if  id['id'] =="owner":
        return str(win_idx+" is the winner")
      
    global verf_check  
    if verf_check == 0:
        for item in price:
            if item != win_idx:
                bid_price = price[item]  
                compile("range.zok", item)
                setup(item)
                witness(item, win_bid, bid_price)
                generate_proof(item)
                with zipfile.ZipFile('archive_zipfile-'+item+'.zip', 'w') as zf:
                    zf.write('proof.json', compress_type =zipfile.ZIP_DEFLATED)
                    zf.write('verification.key',compress_type =zipfile.ZIP_DEFLATED)


        verf_check = 1
    return str(os.getcwd()+'/'+ 'archive_zipfile-'+ id['id']+'.zip')
       

@app.get("/list")
async def list_bidders() -> dict:  
    return bids

@app.get("/open_list")
async def open_list() -> dict:  
    return price 

@app.get('/stored_list')   
async def stored_list() ->dict:
    return stored  
