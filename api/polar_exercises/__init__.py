import json
import urllib.parse
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

    # Optional flags: samples, zones, route
    samples = req.params.get("samples", "false").lower() == "true"
    zones = req.params.get("zones", "false").lower() == "true"
    route = req.params.get("route", "false").lower() == "true"

    qs = urllib.parse.urlencode({
        "samples": str(samples).lower(),
        "zones": str(zones).lower(),
        "route": str(route).lower(),
    })

    url = f"https://www.polaraccesslink.com/v3/exercises?{qs}"

    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as resp:
            payload = resp.read().decode("utf-8")
            return func.HttpResponse(payload, status_code=resp.status, mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"ok": False, "error": "fetch_failed", "detail": str(e)}),
            status_code=500,
            mimetype="application/json",
        )
