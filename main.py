import os
from aws_lambda_powertools import Logger
from auth import open_session, end_session
from data import get_all_tables

logger = Logger()


def main() -> None:
    logger.info(f"Script started")

    sf = open_session()
    if sf is None:
        logger.error("Session is None")
        return

    logger.info(f"Session: {sf}")

    if not os.path.exists("./csv"):
        os.makedirs("./csv")

    if not os.path.exists("./failed"):
        os.makedirs("./failed")

    output = get_all_tables(sf)

    logger.info(f"Output: {output}")
    end_session(sf)
    logger.info("Script ended")


main()
