from web3 import Web3
import requests
import sys
import json

url = "http://0.0.0.0:8000"

headers = {
    'Content-Type':'application/json',
}
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
if __name__ == "__main__":
    print("----------Menu----------")
    print("1: List current bidding")
    print("2: Finalize auction") 
    print("3: Print open bids")
    print("4: Announce Winner") 
    print("5: Finish the auction program") 
    print("6: Check in solidity")
    print("------------------------") 
    
    while True:
        menu = input("Type the menu number you want: ")
        if menu == "5":
            break      
        if menu == "1": 
            data = requests.get(url+"/list").json()
            print("Now, there are "+ str(len(data))+" bidders!")
            print("Name".ljust(8) , "bid_x".ljust(10) , "bid_y".ljust(10))   
            for item in data:
                print(item['id'].ljust(8),     item['bid_x'].ljust(10),item['bid_y'].ljust(10)) 
        elif menu == "2":
            data = requests.get(url+"/close") 
            print("Closed the auction")
        elif menu == "3":
            r = requests.get(url+"/open_list").json()
            print("Name".ljust(10), "Price")
            for item in r:
                print(item.ljust(10),r[item])
        elif menu == "4":
            r = requests.post(url+'/get_win', data=json.dumps({'id':"owner"}), headers=headers).json()
            print(r)
        elif menu =="6":
            contract = web3.eth.contract(address='0xD6c5AfCf3c48D5718be0A3B50E42d9ad420ebDa4', abi=abi) 
            res = contract.functions.receiveBid().call() 
            for item in res:
                print(item)
        elif menu == "7":
             data = requests.get(url+"/stored_list").json()
             print(data)