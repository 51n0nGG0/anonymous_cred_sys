from fastapi import FastAPI
import requests
from models.schemas import (
    VerifyRequest
)

from crypto.rsa_verify import verify

app = FastAPI(title="Verifier API")

ISSUER_URL = "http://127.0.0.1:8000"

def get_public_key():
    r = requests.get(f"{ISSUER_URL}/public-key")
    data = r.json()
    return int(data["N"]), int(data["E"])

@app.post("/verify")
def verify_credential(req: VerifyRequest):
    n, e = get_public_key()
    
    sn = int(req.sn)
    signature = int(req.signature)
    
    is_valid = verify(sn, signature, e, n)
    
    return {
        "valid": is_valid
    }