
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"status": "backend alive"}),
        status_code=200,
        mimetype="application/json"
    )
