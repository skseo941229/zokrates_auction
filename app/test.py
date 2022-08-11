from Zokrates_prover import *
import os

compile("range.zok", "Sukyung")
setup("Sukyung")
witness("Sukyung", 100, 10)
#print("Hello")
generate_proof("Sukyung")