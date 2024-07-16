from sqladmin import Admin
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from common.security import OKTA_CONFIG, OKTA_BASE_URL

class CustomAdmin(Admin):
    """Admin panel customized with self-hosted Okta login widget."""
    async def login(self, request: Request) -> Response:
        assert self.authentication_backend is not None
        context = {
            "baseUrl": OKTA_BASE_URL,
            "clientId": OKTA_CONFIG["client_id"],
            "issuer": OKTA_CONFIG["issuer"],
            "state": OKTA_CONFIG["admin_state"],
            "nonce": OKTA_CONFIG["nonce"],
            "scopes": OKTA_CONFIG["scopes"],
            "redirectUri": OKTA_CONFIG["redirect_uri"],
        }
        token = request.query_params.get("token")
        if token:
            if await self.authentication_backend.login(request):
                return RedirectResponse(request.url_for("admin:index"), status_code=302)
            else:
                return RedirectResponse(request.url_for("admin:login"), status_code=302)

        if request.method == "GET":
            return await self.templates.TemplateResponse(request, "login.html", context)
