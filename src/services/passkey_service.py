from typing import Any
from src.models import (
    UserEntity,
    PasskeyVerifModel,
    CredentialEntity,
    ErrorResponse
)
from src.utils import Singleton
from webauthn import (
    base64url_to_bytes,
    generate_authentication_options,
    options_to_json,
    generate_registration_options,
    verify_registration_response,
    verify_authentication_response,
)

from webauthn.registration.verify_registration_response import VerifiedRegistration
from webauthn.authentication.verify_authentication_response import (
    VerifiedAuthentication,
)

from webauthn.helpers.structs import (
    AttestationConveyancePreference,
    AuthenticatorAttachment,
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialHint,
    ResidentKeyRequirement,
    UserVerificationRequirement,
    PublicKeyCredentialCreationOptions,
)
from email_validator import validate_email, EmailNotValidError
from webauthn.helpers.cose import COSEAlgorithmIdentifier


class PasskeyService(metaclass=Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.saved: UserEntity = UserEntity()
        self.cred: CredentialEntity = CredentialEntity()
        self.rp_id: str = "tester.com"
        self.rp_name: str = "Backend Tester"
        self.timeout = 12000
        self.allowed_origins = [
            "http://localhost:4200",
        ]

    def register_options(self, user: UserEntity) -> PublicKeyCredentialCreationOptions | dict[str, Any]:
        try:
            email = validate_email(user.email, check_deliverability=False).normalized
        except EmailNotValidError as e:
            # email is not valid, raise an error
            return ErrorResponse(error=str(e)).__dict__

        self.saved = user

        return generate_registration_options(
            rp_id=self.rp_id,
            rp_name=self.rp_name,
            user_id=user.user_id.encode("utf-8"),
            user_name=email,
            user_display_name=user.username,
            attestation=AttestationConveyancePreference.DIRECT,
            authenticator_selection=AuthenticatorSelectionCriteria(
                authenticator_attachment=AuthenticatorAttachment.PLATFORM,
                resident_key=ResidentKeyRequirement.REQUIRED,
            ),
            supported_pub_key_algs=[
                COSEAlgorithmIdentifier.ECDSA_SHA_512,
            ],
            timeout=self.timeout,
            hints=[
                PublicKeyCredentialHint.SECURITY_KEY,
                PublicKeyCredentialHint.CLIENT_DEVICE,
            ],
            # TODO: have this setting being configured from the database.
            exclude_credentials=[
                #  PublicKeyCredentialDescriptor(
                #      id=b"1234567890",
                #      transports=[AuthenticatorTransport.INTERNAL],
                #      type=PublicKeyCredentialType.PUBLIC_KEY
                #  )
            ],
        )

    def verify_signup_passkey(self, creds: PasskeyVerifModel) -> VerifiedRegistration:
        resp = verify_registration_response(
            credential=creds.credential.__dict__,
            expected_challenge=base64url_to_bytes(creds.expected_challenge),
            expected_rp_id=self.rp_id,
            expected_origin=self.allowed_origins,
            require_user_verification=True,
            supported_pub_key_algs=[
                COSEAlgorithmIdentifier.ECDSA_SHA_512,
            ],
        )

        self.cred = CredentialEntity(
            id=creds.credential.id,
            user_id=creds.user_id,
            credential_id=resp.credential_id.decode("utf-8"),
            credential_public_key=resp.credential_public_key.decode("utf-8"),
            sign_count=resp.sign_count,
            credential_device_type=resp.credential_device_type,
            credential_backed_up=resp.credential_backed_up,
            transports=creds.credential.response.transports,
        )

        return resp

    def authenticate_options(self):
        complex_authentication_options = generate_authentication_options(
            rp_id=self.rp_id,
            timeout=self.timeout,
            # TODO: have this setting being configured from the database.
            allow_credentials=[
                #  PublicKeyCredentialDescriptor(
                #      id=b"1234567890",
                #      transports=[AuthenticatorTransport.INTERNAL],
                #      type=PublicKeyCredentialType.PUBLIC_KEY
                #  )
            ],
            user_verification=UserVerificationRequirement.REQUIRED,
        )

        return options_to_json(complex_authentication_options)

    def verify_authentication_passkey(self, creds: PasskeyVerifModel) -> VerifiedAuthentication:
        verif = verify_authentication_response(
            credential=creds.credential.__dict__,
            expected_challenge=base64url_to_bytes(creds.expected_challenge),
            expected_rp_id=self.rp_id,
            expected_origin=self.allowed_origins,
            credential_public_key=base64url_to_bytes(
                creds.credential.response.clientDataJSON
            ),
            credential_current_sign_count=0,
            require_user_verification=True,
        )

        self.cred.sign_count = verif.new_sign_count
        self.cred.credential_device_type = verif.credential_device_type
        self.cred.credential_backed_up = verif.credential_backed_up

        return verif
