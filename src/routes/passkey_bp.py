from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag

from src.models import UserEntity, PasskeyVerifModel
from src.controllers import PasskeyController

bp = APIBlueprint("passkey", __name__, url_prefix="/passkey", doc_ui=True)


@bp.errorhandler(400)
def resource_not_found(e: Exception):
    return jsonify(error=str(e)), 400


@bp.post("/register-passkey", summary="Generate register passkey options", tags=[Tag(name="Passkey")])
def register_passkey(body: UserEntity):
    return PasskeyController().register_passkey(body)


@bp.post("/login-passkey", summary="Generate login passkey options", tags=[Tag(name="Passkey")])
def login_passkey():
    return PasskeyController().authenticate_passkey()


@bp.post("/verify-login-passkey", summary="Verify login passkey options", tags=[Tag(name="Passkey")])
def verify_login_passkey(body: PasskeyVerifModel):
    return PasskeyController().verify_auth_passkey(body)


@bp.post("/verify-register-passkey", summary="Verify register passkey options", tags=[Tag(name="Passkey")])
def verify_register_passkey(body: PasskeyVerifModel):
    return PasskeyController().verify_signup_passkey(body)
