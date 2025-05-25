from src.models import (
    UserEntity,
    PasskeyVerifModel
)
from src.services import PasskeyService
from src.utils import Singleton


class PasskeyController(metaclass=Singleton):
    def __init__(self):
        self.passkey_service = PasskeyService()

    def register_passkey(self, user: UserEntity):
        return self.passkey_service.register_options(user)

    def authenticate_passkey(self):
        return self.passkey_service.authenticate_options()

    def verify_signup_passkey(self, creds: PasskeyVerifModel):
        return self.passkey_service.verify_signup_passkey(creds)

    def verify_auth_passkey(self, creds: PasskeyVerifModel):
        return self.passkey_service.verify_authentication_passkey(creds)
