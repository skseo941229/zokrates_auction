import os

def verify():
    os.system("zokrates verify")
    return
def export_verify():
    os.system("zokrates export-verifier")
    return 