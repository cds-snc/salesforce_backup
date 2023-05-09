import csv

from typing import Any
from simple_salesforce import Salesforce
from aws_lambda_powertools import Logger
from utils import query_all, get_all_fields_for_object
from cleanup import cleanup_records, filter_out_sobjects

logger = Logger()
PAGE_SIZE = 200

def get_all_objects(session: Salesforce) -> list[dict[str, Any]]:
    """Gets all objects from Salesforce

    Args:
        session (Salesforce): Authenticated

    Returns:
        list[dict[str, Any]]: List of objects

    """
    logger.info("Getting all objects")
    query = "SELECT SObjectType FROM ObjectPermissions GROUP BY SObjectType ORDER BY SObjectType ASC"
    results = query_all(session, query)
    filter_out_sobjects(results)
    return query_all(session, query)


def build_query_all_records(sobj, page, offset):
    return f"SELECT FIELDS(ALL) FROM {sobj} ORDER BY Id LIMIT {page} OFFSET {offset}"


def get_all_records(session: Salesforce, sobj: str) -> list[dict[str, Any]]:
    """Gets all records from Salesforce

    Args:
        session (Salesforce): Authenticated
    """

    offset = 0
    logger.info(f"Getting all records for {sobj}")

    retval = []

    query = build_query_all_records(sobj, PAGE_SIZE, offset)
    logger.debug(f"Query: {query}")
    results = query_all(session, query)

    while len(results) != 0:
        retval.extend(results)
        offset += PAGE_SIZE
        query = build_query_all_records(sobj, PAGE_SIZE, offset)
        logger.debug(f"Query: {query}")
        results = query_all(session, query)

    return retval


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


def get_all_tables(session: Salesforce) -> list[dict[str, Any]]:
    """Gets all tables from Salesforce

    Args:
        session (Salesforce): Authenticated
    """

    result = get_all_objects(session)
    sObjects = [record["SobjectType"] for record in result]
    sObjects = filter_out_sobjects(sObjects)
    logger.debug(f"sObjects: {sObjects}")

    fields = get_all_fields_for_object(session, "Account")
    logger.debug(f"Fields: {fields}")

    for object in sObjects:
        records = get_all_records(session, object)

        if not records:
            logger.info(f"No records found for {object}")
            continue


        records = cleanup_records(records)

        try:
            write_dict_to_csv(session, records, object)
        except Exception as e:
            logger.error(f"Error writing {object} to CSV: {e}")
            write_dict_to_file(records, object)
