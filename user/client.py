import requests
import secrets

ISSUER_URL = "http://127.0.0.1:8000"

def modinv(r, N):
    return pow(r, -1, N)

def get_public_key():
    r = requests.get(f"{ISSUER_URL}/public-key")
    data = r.json()
    return int(data["N"]), int(data["E"])

def generate_sn():
    return secrets.randbits(256)

def blind_message(m, N, e):
    while True:
        r = secrets.randbelow(N)
        if(r > 1):
            try:
                r_inv = modinv(r, N)
                break
            except:
                continue
    blinded = (m*pow(r, e, N)) % N
    return blinded, r, r_inv

def request_signature(blinded):
    r = requests.post(
        f"{ISSUER_URL}/blind-sign",
        json={"blinded_message": str(blinded)}
    )
    data = r.json()
    return int(data["blind_signature"])

def unblind(signature_blinded, r_inv, N):
    return (signature_blinded*r_inv) % N

def main():
    # 1. Obtenemos la clave pública
    N, e = get_public_key()
    # 2. Obtenemos el SN
    SN = generate_sn()
    # 3. Ocultamos el mensaje
    blinded, r, r_inv = blind_message(SN, N, e)
    # 4. Enviamos el mensaje a cifrar
    signature_blinded = request_signature(blinded)
    # 5. Desocultamos la firma
    signature = unblind(signature_blinded, r_inv, N)
    
    print("SN:", SN)
    print("SIGNATURE:", signature)

if __name__ == "__main__":
    main()