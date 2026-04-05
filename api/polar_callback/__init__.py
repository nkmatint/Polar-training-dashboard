import os
import json
import base64
import urllib.parse
import urllib.request
import azure.functions as func

from .token_store import save_token


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Receive OAuth2 code and exchange it for access token."""
    error = req.params.get("error")
    if error:
        return func.HttpResponse(
            json.dumps({"connected": False, "error": error}),
            status_code=400,
            mimetype="application/json",
        )

    code = req.params.get("code")
    if not code:
        return func.HttpResponse(
            json.dumps({"connected": False, "error": "missing_code"}),
            status_code=400,
            mimetype="application/json",
        )

    client_id = os.environ["POLAR_CLIENT_ID"]
    client_secret = os.environ["POLAR_CLIENT_SECRET"]
    redirect_uri = os.environ["POLAR_REDIRECT_URI"]

    token_url = "https://polarremote.com/v2/oauth2/token"

    basic = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")

    body = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        token_url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json;charset=UTF-8",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"connected": False, "error": "token_exchange_failed", "detail": str(e)}),
            status_code=500,
            mimetype="application/json",
        )

    access_token = payload.get("access_token")
    x_user_id = payload.get("x_user_id")

    if not access_token:
        return func.HttpResponse(
            json.dumps({"connected": False, "error": "missing_access_token", "payload": payload}),
            status_code=500,
            mimetype="application/json",
        )

    save_token({
        "access_token": access_token,
        "x_user_id": x_user_id,
        "token_type": payload.get("token_type"),
        "expires_in": payload.get("expires_in"),
        "scope": payload.get("scope"),
    })

    return func.HttpResponse(
        json.dumps({"connected": True, "x_user_id": x_user_id}),
        status_code=200,
        mimetype="application/json",
    )
