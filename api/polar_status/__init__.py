import json
import azure.functions as func

from .token_store import load_token


def main(req: func.HttpRequest) -> func.HttpResponse:
    data = load_token()
    return func.HttpResponse(
        json.dumps({
            "connected": bool(data.get("access_token")),
            "x_user_id": data.get("x_user_id"),
            "scope": data.get("scope"),
        }),
        status_code=200,
        mimetype="application/json",
    )
