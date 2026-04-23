from pydantic import BaseModel

class BlindSignRequest(BaseModel):
    blinded_message: str
    
class BlindSignResponse(BaseModel):
    blind_signature: str
    
class PublicKeyResponse(BaseModel):
    N: str
    E: str
    
class VerifyRequest(BaseModel):
    sn: str
    signature: str