import json
import azure.functions as func

from .token_store import clear_token


def main(req: func.HttpRequest) -> func.HttpResponse:
    clear_token()
    return func.HttpResponse(
        json.dumps({"cleared": True}),
        status_code=200,
        mimetype="application/json",
    )
