from pydantic import BaseModel, Field


class PKResponseObj(BaseModel):
    attestationObject: str = Field(default="")
    clientDataJSON: str = Field(default="")
    transports: list[str] = Field(default_factory=list)
    authenticatorData: str = Field(default="")
    signature: str = Field(default="")
    userHandle: str = Field(default="")


class PKCredentialObj(BaseModel):
    id: str = Field(default="")
    rawId: str = Field(default="")
    response: PKResponseObj
    type: str = Field(default="")
    clientExtensionResults: dict
    authenticatorAttachment: str = Field(default="")

class PasskeyVerifModel(BaseModel):
    user_id: str = Field(default="")
    credential: PKCredentialObj
    expected_challenge: str = Field(default="")
