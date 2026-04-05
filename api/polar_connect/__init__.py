import os
import json
import urllib.parse
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Redirect user to Polar OAuth2 authorization endpoint."""
    # Provide helpful errors instead of generic HTTP 500
    missing = []
    for k in ["POLAR_CLIENT_ID", "POLAR_REDIRECT_URI"]:
        if not os.environ.get(k):
            missing.append(k)

    if missing:
        return func.HttpResponse(
            json.dumps({
                "ok": False,
                "error": "missing_app_settings",
                "missing": missing,
                "where_to_set": "Azure Portal → Static Web App → Configuration → Application settings"
            }),
            status_code=500,
            mimetype="application/json",
        )

    client_id = os.environ["POLAR_CLIENT_ID"]
    redirect_uri = os.environ["POLAR_REDIRECT_URI"]

    # Optional anti-CSRF state (single-user MVP)
    state = "mvp-single-user"

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        # If scope is omitted, Polar asks consent for all scopes linked to the client.
        "scope": "accesslink.read_all",
        "state": state,
    }

    url = "https://flow.polar.com/oauth2/authorization?" + urllib.parse.urlencode(params)
    return func.HttpResponse(status_code=302, headers={"Location": url})
