import os
import urllib.parse
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Redirect user to Polar OAuth2 authorization endpoint."""
    client_id = os.environ["POLAR_CLIENT_ID"]
    redirect_uri = os.environ["POLAR_REDIRECT_URI"]

    # Optional anti-CSRF state (single-user MVP)
    state = "mvp-single-user"

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "accesslink.read_all",
        "state": state,
    }

    url = "https://flow.polar.com/oauth2/authorization?" + urllib.parse.urlencode(params)
    return func.HttpResponse(status_code=302, headers={"Location": url})
