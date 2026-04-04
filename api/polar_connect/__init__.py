import os
import urllib.parse
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    client_id = os.environ["POLAR_CLIENT_ID"]
    redirect_uri = os.environ["POLAR_REDIRECT_URI"]

    # Polar authorization endpoint (OAuth2 authorization code flow)
    # response_type=code is the only supported response type. [1](https://azure.microsoft.com/en-us/pricing/details/functions/)
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        # scope is optional; if omitted, user is asked to grant all client scopes. [1](https://azure.microsoft.com/en-us/pricing/details/functions/)
        "scope": "accesslink.read_all",
        # optional anti-CSRF state
        "state": "dev-single-user"
    }

    url = "https://flow.polar.com/oauth2/authorization?" + urllib.parse.urlencode(params)

    return func.HttpResponse(status_code=302, headers={"Location": url})
