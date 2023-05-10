import os
from aws_lambda_powertools import Logger
from session_management import open_session, end_session
from data import get_all_tables

TEST_LOCAL = (os.getenv('TEST_LOCAL', 'false') == 'True')

logger = Logger()

def setup_local_env() -> None:
    if not os.path.exists("./csv"):
        os.makedirs("./csv")

    if not os.path.exists("./failed"):
        os.makedirs("./failed")

def main() -> None:
    logger.info(f"Script started")

    sf = open_session()
    if sf is None:
        logger.error("Script ended in error")
        return

    logger.info(f"Session: {sf}")

    if TEST_LOCAL:
        setup_local_env()

    output = get_all_tables(sf)

    logger.info(f"Output: {output}")
    end_session(sf)

    logger.info("Script ended")


main()
