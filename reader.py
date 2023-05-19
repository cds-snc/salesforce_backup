from typing import Any
from simple_salesforce import Salesforce
from aws_lambda_powertools import Logger
from queries import query_all, get_all_fields_for_object
from cleanup import cleanup_records, filter_out_sobjects
from file_writer import write_dict_to_csv, write_dict_to_file

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
    return query_all(session, query)


def build_query_all_records(sobj, page, offset):
    query = f"SELECT FIELDS(ALL) FROM {sobj} ORDER BY Id LIMIT {page} OFFSET {offset}"
    logger.debug(f"Query: {query}")
    return query


def get_all_records(session: Salesforce, sobj: str) -> list[dict[str, Any]]:
    """Gets all records from Salesforce

    Args:
        session (Salesforce): Authenticated
    """

    offset = 0
    logger.debug(f"Getting all records for {sobj}")

    retval = []

    query = build_query_all_records(sobj, PAGE_SIZE, offset)
    results = query_all(session, query)

    while len(results) != 0:
        retval.extend(results)
        offset += PAGE_SIZE
        query = build_query_all_records(sobj, PAGE_SIZE, offset)
        results = query_all(session, query)

    logger.debug(f"Found {len(retval)} records for {sobj}")
    return retval


def get_all_tables(session: Salesforce) -> list[dict[str, Any]]:
    """Gets all tables from Salesforce

    Args:
        session (Salesforce): Authenticated
    """

    result = get_all_objects(session)
    sObjects = [record["SobjectType"] for record in result]
    sObjects = filter_out_sobjects(sObjects)

    for object in sObjects:
        records = get_all_records(session, object)

        if not records:
            continue

        records = cleanup_records(records)

        try:
            write_dict_to_csv(session, records, object)
        except Exception as e:
            logger.error(f"Error writing {object} to CSV: {e}")
            write_dict_to_file(records, object)
