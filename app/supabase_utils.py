from enum import Enum
import logging
from typing import Dict, List, Union

from supabase import create_client, Client

from app.config import settings


# Logging Config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("supabase-utils") 


# Statuses for supallama_apps Supabase table
SUPALLAMA_APP_STATUS: Dict[str, str] = {
    "queued": "Queued",
    "generating_code": "Generating Code",
    "completed": "Completed",
    "errored": "Errored",
}


def get_user_from_supabase_auth(encoded_access_token: str) -> Union[str, None]:
    """
    Passes the JWT to the Supabase server to retrieve the user from the database.
    """

    logger.info("In the get_user_from_supabase_auth utility function")

    if encoded_access_token is None or type(encoded_access_token) is not str:
        logger.error(f"Invalid JWT: {encoded_access_token}")
        return None

    try:
        logger.info("Create a Supabase client using the service role key")
        supabase_client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )

        logger.info("Checking Supabase auth database to verify that the user is logged in")
        supabase_user_response = supabase_client.auth.get_user(encoded_access_token)
        
        logger.info(f"Received the following UserResponse: {supabase_user_response}")
        
        # Return the user's ID
        return supabase_user_response.user.id

    except Exception as error:
        logger.error(error)
        return None


def update_status_of_record_in_supallama_apps_table(supallama_apps_id: int, user_id: str, status: str) -> None:
    """
    Updates a record in the supallama_apps table's status 
    if, and only if, the id and user_id of the record in
    the supallama_apps table "match" (i.e., this record
    was originally created on behalf of the current user)
    """

    logger.info("In the update_status_of_record_in_supallama_apps_table utility function")

    if supallama_apps_id is None or type(supallama_apps_id) is not int or supallama_apps_id < 1: 
        logger.error(f"Invalid supallama_apps_id: {type(supallama_apps_id) } {supallama_apps_id}")
        return None

    if user_id is None or type(user_id) is not str or len(user_id.strip()) == 0:
        logger.error(f"Invalid user_id: {user_id}")
        return None
     
    if status is None or type(status) is not str or len(status.strip()) == 0:
        logger.error(f"Invalid status: {status}")
        return None

    try:
        logger.info("Create a Supabase client using the service role key")
        supabase_client: Client = create_client(
            settings.SUPABASE_URL, 
            settings.SUPABASE_SERVICE_ROLE_KEY
        )

        logger.info(f"Update status to {status} for supallama_apps row ID: {supallama_apps_id} for user_id: {user_id}")
        response = (
            supabase_client.table("supallama_apps")
            .update({
                "app_status": status,
            })
            .eq("id", supallama_apps_id)
            .eq("user_id", user_id)
            .execute()
        ) 
        
        logger.info(f"Update supallama_apps record response: {response}")

        # Return the updated record's data
        return response.data
    except Exception as error:
        logger.error(error)
        return None

     