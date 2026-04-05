import os
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    keys = [
        "POLAR_CLIENT_ID",
        "POLAR_CLIENT_SECRET",
        "POLAR_REDIRECT_URI",
        "POLAR_MEMBER_ID",
    ]

    present = {k: bool(os.environ.get(k)) for k in keys}

    # Never return secrets. For client id and redirect uri we can show masked/preview safely.
    client_id = os.environ.get("POLAR_CLIENT_ID", "")
    redirect_uri = os.environ.get("POLAR_REDIRECT_URI", "")

    preview = {
        "POLAR_CLIENT_ID_preview": (client_id[:6] + "…" + client_id[-4:]) if client_id else "",
        "POLAR_REDIRECT_URI": redirect_uri,
        "POLAR_MEMBER_ID": os.environ.get("POLAR_MEMBER_ID", ""),
    }

    return func.HttpResponse(
        json.dumps({
            "ok": True,
            "present": present,
            "preview": preview,
            "note": "If any required setting is missing, set it in Azure Portal → Static Web App → Configuration → Application settings, then redeploy/restart."
        }),
        status_code=200,
        mimetype="application/json",
    )
