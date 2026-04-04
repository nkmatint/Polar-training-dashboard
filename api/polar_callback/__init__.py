import os
import json
import base64
import urllib.parse
import urllib.request
import azure.functions as func

# MVP storage (Option 1):
# In-memory global var (can reset on cold start/redeploy)
TOKEN_CACHE = {}

def main(req: func.HttpRequest) -> func.HttpResponse:
    code = req.params.get("code")
    error = req.params.get("error")

    if error:
        return func.HttpResponse(
            f"Polar authorization failed: {error}",
            status_code=400
        )

    if not code:
        return func.HttpResponse("Missing code parameter", status_code=400)

    client_id = os.environ["POLAR_CLIENT_ID"]
    client_secret = os.environ["POLAR_CLIENT_SECRET"]
    redirect_uri = os.environ["POLAR_REDIRECT_URI"]

    # Token endpoint is https://polarremote.com/v2/oauth2/token [1](https://azure.microsoft.com/en-us/pricing/details/functions/)
    token_url = "https://polarremote.com/v2/oauth2/token"

    # Basic auth header: base64(client_id:client_secret) [1](https://azure.microsoft.com/en-us/pricing/details/functions/)
    basic = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")

    body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }).encode("utf-8")

    request = urllib.request.Request(
        token_url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json;charset=UTF-8"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return func.HttpResponse(f"Token exchange failed: {str(e)}", status_code=500)

    # payload includes access_token and x_user_id [1](https://azure.microsoft.com/en-us/pricing/details/functions/)
    access_token = payload.get("access_token")
    x_user_id = payload.get("x_user_id")

    if not access_token:
        return func.HttpResponse(f"Token response missing access_token: {payload}", status_code=500)

    # Store token (MVP)
    TOKEN_CACHE["access_token"] = access_token
    TOKEN_CACHE["x_user_id"] = x_user_id

    return func.HttpResponse(
        json.dumps({"connected": True, "x_user_id": x_user_id}),
        status_code=200,
        mimetype="application/json"
    )
