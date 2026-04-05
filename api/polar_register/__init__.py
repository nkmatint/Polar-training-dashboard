import os
import json
import urllib.request
import azure.functions as func

from .token_store import load_token


def main(req: func.HttpRequest) -> func.HttpResponse:
    token = load_token().get("access_token")
    if not token:
        return func.HttpResponse(
            json.dumps({"ok": False, "error": "not_connected"}),
            status_code=401,
            mimetype="application/json",
        )

    # member-id is your own identifier for the user in *your* system.
    # For single-user MVP we take it from env var.
    member_id = os.environ.get("POLAR_MEMBER_ID", "single-user")

    url = "https://www.polaraccesslink.com/v3/users"

    body = json.dumps({"member-id": member_id}).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as resp:
            payload = resp.read().decode("utf-8")
            # response is JSON
            return func.HttpResponse(payload, status_code=resp.status, mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"ok": False, "error": "register_failed", "detail": str(e)}),
            status_code=500,
            mimetype="application/json",
        )
