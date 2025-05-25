from pydantic import BaseModel, Field


class CredentialEntity(BaseModel):
    id: str = Field(default="")
    user_id: str = Field(default="")
    credential_id: str = Field(default="")
    credential_public_key: str = Field(default="")
    sign_count: int = Field(default=0)
    credential_device_type: str = Field(default="")
    credential_backed_up: bool = Field(default=False)
    transports: list[str] = Field(default_factory=list)
