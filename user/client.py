import requests
import secrets

ISSUER_URL = "http://127.0.0.1:8000"

def modinv(r, n):
    return pow(r, -1, n)

def get_public_key():
    r = requests.get(f"{ISSUER_URL}/public-key")
    data = r.json()
    return int(data["N"]), int(data["E"])

def generate_sn():
    return secrets.randbits(256)

def blind_message(m, n, e):
    while True:
        r = secrets.randbelow(n)
        if(r > 1):
            try:
                r_inv = modinv(r, n)
                break
            except:
                continue
    blinded = (m*pow(r, e, n)) % n
    return blinded, r, r_inv

def request_signature(blinded):
    r = requests.post(
        f"{ISSUER_URL}/blind-sign",
        json={"blinded_message": str(blinded)}
    )
    data = r.json()
    return int(data["blind_signature"])

def unblind(signature_blinded, r_inv, n):
    return (signature_blinded*r_inv) % n

def main():
    # 1. Obtenemos la clave pública
    n, e = get_public_key()
    # 2. Obtenemos el SN
    sn = generate_sn()
    # 3. Ocultamos el mensaje
    blinded, r, r_inv = blind_message(sn, n, e)
    # 4. Enviamos el mensaje a cifrar
    signature_blinded = request_signature(blinded)
    # 5. Desocultamos la firma
    signature = unblind(signature_blinded, r_inv, n)
    
    print("SN:", sn)
    print("SIGNATURE:", signature)

if __name__ == "__main__":
    main()