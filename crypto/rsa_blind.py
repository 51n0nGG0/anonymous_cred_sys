from Crypto.PublicKey import RSA

key = RSA.generate(2048)

N = key.n
E = key.e
D = key.d

def get_public_key():
    return {"N": str(N), "E":str(E)}

def blind_sign(blinded_message_int: int) -> int:
    signature = pow(blinded_message_int, D, N)
    return signature

