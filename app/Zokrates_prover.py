import os

def compile(filename, name):
    os.system("zokrates compile -i " + filename + " -o "+name)
    return

def witness(name, price, bidprice):
    os.system("zokrates compute-witness --verbose -i "+name + " -a " + str(price)+ " "+ str(bidprice))
    return

def setup(name):
    os.system("zokrates setup -i "+ name)
    return 

def generate_proof(name):
    os.system("zokrates generate-proof -i "+name)
    return
