from shutil import register_unpack_format
import requests
import sys
import json
import sys
import sys
from pybp.pederson import PedersonCommitment
from pybp.rangeproof import RangeProof
import zipfile
import pickle
from urllib.request import urlretrieve
from web3 import Web3 
import os
import pybitcointools as B
import ast
from functools import reduce
from typing import List, Union, Dict

from pybp.utils import get_blinding_value, get_blinding_vector, getNUMS, modinv, fiat_shamir
from pybp.pederson import PedersonCommitment
from pybp.types import Scalar, Point
from pybp.vectors import Vector, to_bitvector, to_powervector
from pybp.innerproduct import InnerProductCommitment
import logging
from Zokrates_verifier import *
from solcx import compile_standard, install_solc
import json

web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
#logging.basicConfig(level = logging.NOTSET)
url = "http://0.0.0.0:8000"

def verifying( Ap, Sp, T1p, T2p, tau_x, mu, t, proof, V):
        fs_state = b''

        # Compute challenges to find x, y, z
        fs_state, fs_challenge = fiat_shamir(fs_state, [V, Ap, Sp])
        y: Scalar = fs_challenge[0]
        z: Scalar = fs_challenge[1]
        z2 = pow(z, 2, B.N)

        fs_state, fs_challenge = fiat_shamir(fs_state, [T1p, T2p], nret=1)
        x_1 = fs_challenge[0]

        # Construct verification equation (61)
        power_of_ones = to_powervector(1, 32)
        power_of_twos = to_powervector(2, 32)
        yn = to_powervector(y, 32)

        k: Scalar = ((yn @ power_of_ones) * (-z2)) % B.N
        k = (k - (power_of_ones @ power_of_twos) * pow(z, 3, B.N)) % B.N

        gexp: Scalar = (k + z * (power_of_ones @ yn)) % B.N

        lhs = PedersonCommitment(t, b=tau_x).get_commitment()

        rhs = B.multiply(B.G, gexp)
        rhs = B.add_pubkeys(rhs, B.multiply(V, z2))
        rhs = B.add_pubkeys(rhs, B.multiply(T1p, x_1))
        rhs = B.add_pubkeys(rhs, B.multiply(T2p, pow(x_1, 2, B.N)))

        if not lhs == rhs:
            print('(61) verification check failed')
            return False

        # HPrime
        hprime = []
        yinv = modinv(y, B.N)

        for i in range(1, 32 + 1):
            hprime.append(
                B.multiply(getNUMS(32 + i), pow(yinv, i-1, B.N))
            )

        # Reconstruct P
        P = B.add_pubkeys(
            B.multiply(Sp, x_1),
            Ap
        )

        # Add g*^(-z)
        for i in range(32):
            P = B.add_pubkeys(
                B.multiply(getNUMS(i+1), -z % B.N),
                P
            )

        # zynz22n is the exponent of hprime
        zynz22n = (yn * z) + (power_of_twos * z2)

        for i in range(32):
            P = B.add_pubkeys(
                B.multiply(hprime[i], zynz22n[i]),
                P
            )

        fs_state, fs_challenge = fiat_shamir(
            fs_state, [tau_x, mu, t], nret=1)
        uchallenge: Scalar = fs_challenge[0]
        U = B.multiply(B.G, uchallenge)
        P = B.add_pubkeys(
            B.multiply(U, t),
            P
        )

        # P should now be : A + xS + -zG* + (zy^n+z^2.2^n)H'* + tU
        # One can show algebraically (the working is omitted from the paper)
        # that this will be the same as an inner product commitment to
        # (lx, rx) vectors (whose inner product is t), thus the variable 'proof'
        # can be passed into the IPC verify call, which should pass.
        # input to inner product proof is P.h^-(mu)
        p_prime = B.add_pubkeys(
            P,
            B.multiply(getNUMS(255), -mu % B.N)
        )

        a, b, L, R = proof

        iproof = InnerProductCommitment(
            power_of_ones,
            power_of_twos,
            H=hprime,
            U=U
        )

        return iproof.verify_proof(a, b, p_prime, L, R)
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

headers = {
    'Content-Type':'application/json',
}
contract = web3.eth.contract(address='0xD6c5AfCf3c48D5718be0A3B50E42d9ad420ebDa4', abi=abi)
    
if __name__ == "__main__":
    print("----------Menu----------")
    print("0: Enter the value you want to bid")
    print("1: Place your bid")
    print("2: Open bids. ex) name, h_x, h_y, b (blinding factor)") 
    print("3: Check submitted open bid result")
    print("4: Get Winner/Verification") 
    print("5: Finish the program")
    print("------------------------")  
    
    value = 0 
    name = str(sys.argv[1])
    h_x = 0
    h_y = 0
    b = 0
    c_x = 0
    c_y = 0
    
    while True:
        menu = input("Type the menu number you want: ")
        if menu == "5":
            break
        if menu == "0":
            value = input("Type the bid price: ")
            value = int(value)
            rp = RangeProof(32) 
            proofval = value & (2**32 - 1)
            rp.generate_proof(proofval)
            Varg = PedersonCommitment(value, b = rp.gamma)
            h_x, h_y = Varg.h
            b = Varg.b 
            c_x, c_y = Varg.get_commitment()
            print("Your pedersen commitment value is------")
            #logging.debug('Your pedersen commitment value is------')
            print("Bid_x: ", c_x)
            print("Bid_y: ", c_y)
        elif menu == "1": 
            check = input("Want to use above pedersen commitment value you have? y/n: ")
            if check == "y":
                data = {'id': name, 'bid_x': str(c_x), 'bid_y':str(c_y)}
                r = requests.post(url+"/bid", data = json.dumps(data), headers=headers).json()
                if r == "0":
                    print("Your bid is placed")
                else:
                    print("You are not allowed to place bid! We already closed the deals")
            else:
                print("Check menu....")
        elif menu == "2":
            ### Edit here 
            first_check = input("Want to put values? y/n: ")
            r = requests.get(url+"/bfcheck", headers=headers).json() 
            if r == "Please enter your value":
                
                check = input("Want to use h and r value you have? y/n: ")
                if check == "y":
        
                    address = '0xD656fAd2D330bC98f2Fd7D990463397aA81953a2'
                    
                    store_contact = contract.functions.openBid(name, value, h_x,h_y,b).buildTransaction({"chainId": 1337, "gasPrice": web3.toWei('50','gwei'), "from": address, "nonce": web3.eth.getTransactionCount(address)})
                    signed_tx = web3.eth.account.signTransaction(store_contact, private_key='fed3000ead31e8bc837793a406e2f65ea076dd5b224769fa967a854f670bc186')
                    web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                    
                else:
                    print("Check menu....")  
        elif menu == "3":
            print("Check submitted commitment result") 
            r = requests.post(url+"/check", data = json.dumps({'id':name}), headers=headers).json() 
            print(r)
        elif menu == "4":
            print("----Your result-----")
            
            r = requests.post(url+'/get_win', data=json.dumps({'id': name}), headers=headers).json()
            #### Proving key send 
            if r == "You are the winner":
                print(r)
            else:
                urlretrieve("file:///"+r, 'archive_zipfile-'+ name+'.zip')
                with zipfile.ZipFile('archive_zipfile-'+ name+'.zip', 'r') as zip_ref:
                    zip_ref.extractall()
                print("Received the proof")
                verify()
                print("Verification Completed")
                last_check = input("Want to check in solidity? y/n: ")
                if last_check == 'y':
                    export_verify()
                    with open("verifier.sol", "r") as file:
                        verification = file.read()
                    install_solc("0.8.0")

                    compiled_sol = compile_standard(
						{
							"language": "Solidity",
							"sources": {"verifier.sol": {"content": verification}},
							"settings": {
								"outputSelection": {
									"*": {
										"*": [
											"abi",
											"metadata",
											"evm.bytecode",
											"evm.bytecode.sourceMap",
										]  # output needed to interact with and deploy contract
									}
								}
							},
						},
						solc_version="0.8.0",
					)

                    with open("compiler_output.json", "w") as file:
                        json.dump(compiled_sol, file)
      				
                    bytecode = compiled_sol["contracts"]["verifier.sol"]["Verifier"]["evm"]["bytecode"]["object"]
                    abi = json.loads(compiled_sol["contracts"]["verifier.sol"]["Verifier"]["metadata"])["output"]["abi"]

                    with open('abi.json', 'w') as f:
                        json.dump(abi, f)
                    chain_id = 1337
                    address = "0xD656fAd2D330bC98f2Fd7D990463397aA81953a2"
                    private_key = (
						"fed3000ead31e8bc837793a406e2f65ea076dd5b224769fa967a854f670bc186"
					)  # leaving the private key like this is very insecure if you are working on real world project


                    Verification = web3.eth.contract(abi=abi, bytecode=bytecode).constructor().transact({"from": address})
                    tx_receipt = web3.eth.getTransactionReceipt(Verification) 
                    print("Your verifier contract address: " , tx_receipt.contractAddress)
                    print("Deploying verifier Contract!") 
                    os.system("node zokrates_compile.js "+tx_receipt.contractAddress); 


            
            
            
            
            
        
