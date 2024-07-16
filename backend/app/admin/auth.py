from okta_jwt_verifier import JWTUtils
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from common.security import OKTA_CONFIG
from db.session import session
from models.user import User


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        token = request.query_params.get("token")
        claims = JWTUtils.parse_token(token)[1]
        email = claims["sub"]

        user = session().query(User).filter(User.email == email).first()
        if not user or not user.is_superuser:
            return False

        request.session.update({"token": token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        try:
            claims = JWTUtils.parse_token(token)[1]
            JWTUtils.verify_claims(claims, ['aud', 'iss', 'exp'], OKTA_CONFIG['issuer'], OKTA_CONFIG['issuer'])
            email = claims["sub"]

            user = session().query(User).filter(User.email == email).first()
            if not user or not user.logically_tos_accepted or not user.is_superuser:
                return False
        except Exception:
            return False

        return True
