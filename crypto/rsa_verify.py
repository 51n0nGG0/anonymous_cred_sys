def verify(sn:int, signature: int, e: int, n: int):
    check = pow(signature, e, n)
    
    return check == sn
    