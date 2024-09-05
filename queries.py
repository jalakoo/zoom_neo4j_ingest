from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import ClientError
from zoom_model import ZoomModel
from profile_model import Profile
import os
import logging

HOST = os.environ.get("NEO4J_URI")
PASSWORD = os.environ.get("NEO4J_PASSWORD")
USER = os.environ.get("NEO4J_USERNAME", "neo4j")
DATABASE = os.environ.get("NEO4J_DATABASE", "neo4j")


def execute_query(query, params):
    with GraphDatabase.driver(
        HOST, auth=basic_auth(USER, PASSWORD), database=DATABASE
    ) as driver:
        return driver.execute_query(query, params)


def add_profile(data: ZoomModel):

    profile = data.profile
    pid = profile.id

    # Profile/User node
    query = """
    MERGE (p:User {id: $pid})
    SET p = $profile
    """
    params = {
        "pid": pid,
        "profile": profile.model_dump(),
    }
    try:
        execute_query(query, params)
    except ClientError as e:
        if e.code == ClientError.Schema.ConstraintValidationFailed:
            # profile already exists
            pass
        else:
            # If it's a different ClientError, handle it as usual
            raise Exception(f"Error adding profile': {e}")
    except Exception as e:
        raise Exception(f"Error adding profile with data: {profile}: {e}")

    # pastMeetings
    pastMeetings = data.pastMeetings
    if pastMeetings is None:
        logging.info(
            f"No past meetings for profile with id: {pid}. Data: {data.__dict__}"
        )
    else:
        # Meetings + Profile-Meeting relationships
        query = """
        MATCH (pr:User {id: $pid})
        WITH pr
        UNWIND $pastMeetings as meeting
            MERGE (m:Meeting {uuid: meeting.details.uuid})
            SET m += meeting.details
            SET m += COALESCE(meeting.summary, {})
            MERGE (pr)-[:HOSTED]->(m)
        RETURN pr, m
        """
        params = {
            "pid": pid,
            "pastMeetings": [meeting.model_dump() for meeting in pastMeetings],
        }
        try:
            _, _, _ = execute_query(query, params)
        except Exception as e:
            raise Exception(f"Error adding pastMeetings: {e}")

        # TODO:
        # Import summary details separately as their own nodes

        # Participants where participant has a user_id. Participants might not have an id or user_id for anonymous users. user_names are also not unique. All participants are given a unique participant_uuid per meeting.
        query = """
        UNWIND $pastMeetings as meeting
        MATCH (m:Meeting {uuid: meeting.details.uuid})
        WITH m, meeting
        UNWIND meeting.participants as participant
            WITH participant
            WHERE participant.participant_uuid IS NOT NULL
            MERGE (p:Participant {participant_uuid: participant.participant_uuid})
            SET p += participant
        """
        try:
            execute_query(query, params)
        except Exception as e:
            raise Exception(f"Error adding pastMeeting's participants to meetings: {e}")

        # Participant-Meeting relationships for participants.
        query = """
        UNWIND $pastMeetings as meeting
        MATCH (m:Meeting {uuid: meeting.details.uuid})
        WITH m, meeting
        UNWIND meeting.participants as participant
            MATCH (p:Participant {participant_uuid: participant.participant_uuid})
            MERGE (p)-[:ATTENDED]->(m)
        """
        try:
            execute_query(query, params)
        except Exception as e:
            raise Exception(
                f"Error creating participants to meeting relationships: {e}"
            )

        # User-Participant relationship if there is a match
        query = """
        UNWIND $pastMeetings as meeting
        UNWIND meeting.participants as participant
            WITH participant
            WHERE participant.id IS NOT NULL
            MATCH (p:User {id: participant.id})
            MATCH (pa:Participant {id: participant.id})
            MERGE (p)-[:IS]->(pa)
        """
        try:
            execute_query(query, params)
        except Exception as e:
            raise Exception(
                f"Error adding Connecting participants with existing User profile: {e}"
            )

        # Recordings and Recording-Meeting relationships
        query = """
        UNWIND $pastMeetings as meeting
        MATCH (m:Meeting {uuid: meeting.details.uuid})
        WITH m, meeting
        UNWIND COALESCE(meeting.recordings, []) as recording
            MERGE (r:Recording {id: recording.id})
            ON CREATE SET r += recording
            MERGE (m)-[:HAS]->(r)
        """
        try:
            execute_query(query, params)
        except Exception as e:
            raise Exception(f"Error adding pastMeeting's recordings for meeting: {e}")
