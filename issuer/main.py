from fastapi import FastAPI
from crypto.rsa_blind import get_public_key, blind_sign
from models.schemas import (
    BlindSignRequest,
    BlindSignResponse,
    PublicKeyResponse
)

app = FastAPI(tittle="Issuer API")

@app.get("/public-key", response_model=PublicKeyResponse)
def public_key():
    return get_public_key()

@app.post("/blind-sign", response_model=BlindSignResponse)
def sign_blinded(req:BlindSignRequest):
    blinded_int = int(req.blinded_message)
    
    signature = blind_sign(blinded_int)
    
    return BlindSignResponse(
        blind_signature=str(signature)
    )