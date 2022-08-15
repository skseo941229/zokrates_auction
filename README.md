# Sealed bid auction using zokrates
This is the final step of a progressive sealed-bid auction. For the first and second step, please refer to https://github.com/skseo941229/pure_auction_v1 and https://github.com/skseo941229/sc_auction_v2.   

## Description

In this part, zokrates was used to generate proof and verify this proof. It is implausible to do computation on Ethereum not only because of the gas fee but because of privacy issues. In blockchain, people can view all the information. Thus, zokrates can help solve this problem.  

## Getting Started

### Dependencies

* Ganache

### Installing

* pybp package (https://github.com/kendricktan/pybp)
* web3 package
```
pip install web3
```
* zokrates (https://zokrates.github.io/) 
  To use zokrates globally, add export PATH = ~ to zshrc file. 

### Executing program
* Executing the auction: 
```
python auction.py
```

* To query auction status, execute the auction_info:
```
python auction_info.py
```

* To be a bidder of a program, execute the bidder:
```
python bidder.py <bidder_name>
```
