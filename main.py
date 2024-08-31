from basicauth import decode
from typing import List, Optional
from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import ClientError
from pydantic import BaseModel, Field
from zoom_model import ZoomModel
from queries import add_profile
import functions_framework
import json
import os
import logging


def ingest_zoom(model: ZoomModel):
    try:
        add_profile(model.profile)
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

    # Check payload is a JSON list of dictionaries
    if not isinstance(payload, list) or not all(
        isinstance(item, dict) for item in payload
    ):
        return "Invalid payload: expected a list of dictionaries", 400

    # Process each item in the list
    results = []
    for item in payload:
        try:
            ddata = ZoomModel(**item)
            results.append(ingest_zoom(ddata))
        except Exception as e:
            results.append(f"Invalid payload: {e}")

    return results, 200
