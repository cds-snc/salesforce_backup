from typing import Any, Optional
from simple_salesforce import Salesforce
from aws_lambda_powertools import Logger

logger = Logger()


def query_one(session: Salesforce, query: str) -> Optional[dict[str, Any]]:
    """Execute an SOQL query that expects to return a single record.

    Args:
        query (str): The SOQL query to execute
        session (Salesforce): Authenticated Salesforce session

    Returns:
        dict[str, Any]: The result of the query or None
    """
    result = None
    try:
        results = session.query(query)
        if results.get("totalSize") == 1:
            result = results.get("records")[0]
        else:
            logger.warn(f"Salesforce no results found for query {query}")
    except Exception as ex:
        logger.error(f"Salesforce query {query} failed: {ex}")
    return result


def query_all(session: Salesforce, query: str) -> list[dict[str, Any]]:
    """Execute an SOQL query that expects to return multiple records.

    Args:
        query (str): The SOQL query to execute
        session (Salesforce): Authenticated Salesforce session

    Returns:
        list[dict[str, Any]]: The result of the query or an empty list
    """

    result = []
    try:
        results = session.query_all(query)
        if results.get("totalSize") > 0:
            result = results.get("records")
        else:
            logger.warn(f"Salesforce no results found for query {query}")
    except Exception as ex:
        logger.error(f"Salesforce query {query} failed: {ex}")
    return result


def get_all_fields_for_object(session: Salesforce, name: str) -> list[dict[str, Any]]:
    """Gets all the fields for a given object

    Args:
        session (Salesforce): Authenticated
        name (str): Name of the object

    Returns:
        list[dict[str, Any]]: List of fields
    """
    logger.info("Getting all fields for object")

    field_names = []
    fields = session.__getattr__(name).describe()["fields"]

    for field in fields:
        field_names.append(field["name"])

    logger.debug(f"Fields: {field_names}")
    return field_names
