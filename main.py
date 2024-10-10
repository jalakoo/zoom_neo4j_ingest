from basicauth import decode
from zoom_model import ZoomModel
from queries import add_profile
import functions_framework
import os
import logging

logging.basicConfig(level=logging.DEBUG)

logging.getLogger("neo4j.io").setLevel(logging.ERROR)
logging.getLogger("neo4j.pool").setLevel(logging.ERROR)


def ingest_zoom(model: ZoomModel):
    try:
        add_profile(model)
        return f"Successfully added profile with id: `{model.profile.id}`"
    except Exception as e:
        return f"Error adding profile with id: {model.profile.id}: {e}"


@functions_framework.http
def ingest(request):

    # Optional Basic Auth
    basic_user = os.environ.get("BASIC_AUTH_USER", None)
    basic_password = os.environ.get("BASIC_AUTH_PASSWORD", None)
    if basic_user and basic_password:
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            return "Missing authorization credentials", 401
        try:
            request_username, request_password = decode(auth_header)
            if request_username != basic_user or request_password != basic_password:
                return "Unauthorized", 401
        except Exception as e:
            logging.error(
                f"Problem parsing authorization header: {auth_header}: ERROR: {e}"
            )
            return f"Problem with Authorization credentials: {e}", 400

    payload = request.get_json(silent=True)

    # Single item payload?
    if not isinstance(payload, list):
        try:
            ddata = ZoomModel(**payload)
            logging.debug(f"Processing payload with {len(ddata.pastMeetings)} meetings")
            return ingest_zoom(ddata)
        except Exception as e:
            return f"Invalid payload: {e}", 400

    # Process multiple item payloads
    results = []
    for item in payload:
        try:
            ddata = ZoomModel(**item)
            logging.debug(f"Processing payload with {len(ddata.pastMeetings)} meetings")
            results.append(ingest_zoom(ddata))
        except Exception as e:
            results.append(f"Invalid payload: {e}")

    print(f"Ingest complete: {results}")
    return results, 200
