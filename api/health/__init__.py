
import json

def main(req):
    return {
        "status": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({ "status": "backend alive" })
    }
