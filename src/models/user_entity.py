from pydantic import BaseModel, Field


class UserEntity(BaseModel):
    user_id: str = Field(default="")
    username: str = Field(default="")
    email: str = Field(default="")
    password: str = Field(default="")
