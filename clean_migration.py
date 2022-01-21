from email.errors import InvalidMultipartContentTransferEncodingDefect
import requests
import json
from migrate_teams import retrieve_teams_id
from migrate_teams import TARGET_KEY, base_url, headers
import logging
from commons.utils import setup_logging

logger = setup_logging()

def cleanup_target(api_key):
    logger.info("Retrieving teams ID to be cleaned up")

    id_list = retrieve_teams_id(api_key)
    logger.info(f"Teams ID list: {id_list}")
    
    # iterate over each ID to DELETE
    for item in id_list:
        url = f"{base_url}/{item}"
        
        #Simulate a wrong credential being passed to test error status_code handling
        '''api_key += "zz"
        headers["Authorization"] = f"Token token={api_key}"'''

        response = requests.request("DELETE", url, headers=headers)
        
        if response.status_code == 204:
            logger.info(f"Team '{item}' successfully deleted")
        elif response.status_code == 401:
            logger.error("Wrong credentials provided")
        elif response.status_code == 402:
            logger.error("Account does not have the abilities to perform the action")

if __name__ == '__main__':
    logger.info("Starting migration cleanup for teams entity")
    cleanup_target(TARGET_KEY)