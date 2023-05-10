from typing import Any
import csv
from simple_salesforce import Salesforce
from aws_lambda_powertools import Logger
from queries import get_all_fields_for_object

logger = Logger()

def write_dict_to_csv(
    session: Salesforce, dicts: list[dict[str, Any]], sobj: str
) -> None:
    """Writes a dictionary to a CSV file

    Args:
        dict (dict[str, Any]): Dictionary to write
        filename (str): Filename to write to
    """
    columns = get_all_fields_for_object(session, sobj)

    logger.info(f"Writing {sobj}.csv")
    with open(f"./csv/{sobj}.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(dicts)


def write_dict_to_file(dicts: list[dict[str, Any]], filename: str) -> None:
    """Writes a dictionary to a file

    Args:
        dict (dict[str, Any]): Dictionary to write
        filename (str): Filename to write to
    """

    logger.info(f"Writing {filename}.txt")
    with open(f"./failed/{filename}.txt", "w") as csvfile:
        for data in dicts:
            csvfile.write(str(data) + "\n")