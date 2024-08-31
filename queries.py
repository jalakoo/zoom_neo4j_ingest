from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import ClientError
from profile_model import Profile
import os
import logging

HOST = os.environ.get("NEO4J_URI")
PASSWORD = os.environ.get("NEO4J_PASSWORD")
USER = os.environ.get("NEO4J_USER", "neo4j")
DATABASE = os.environ.get("NEO4J_DATABASE", "neo4j")


def execute_query(query, params):
    with GraphDatabase.driver(
        HOST, auth=basic_auth(USER, PASSWORD), database=DATABASE
    ) as driver:
        return driver.execute_query(query, params)


def add_profile(profile: Profile):

    pid = profile.id

    query = """
    MERGE (p:Profile {id: $pid})
    SET p = $profile
"""
    params = {
        "pid": pid,
        "profile": profile.model_dump(),
    }
    return execute_query(query, params)
