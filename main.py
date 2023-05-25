import os
from aws_lambda_powertools import Logger
from session_management import open_session, end_session
from reader import get_all_tables

# TEST_LOCAL = os.getenv("TEST_LOCAL", "false").lower() == "true"

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

    setup_local_env()

    get_all_tables(sf)

    end_session(sf)

    logger.info("Script ended")


main()
