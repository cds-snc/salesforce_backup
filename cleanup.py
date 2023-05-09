from typing import Any
from copy import deepcopy

UNSUPPORTED_SOBJS = ["Scorecard", "ScorecardAssociation", "ScorecardMetric", "UserExternalCredential", "WebCartDocument"]

def cleanup_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = remove_unneeded_fields(records, ["attributes"])
    records = replace_newlines_in_dict_values(records)
    return records


def replace_newlines_in_dict_values( dicts: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Replaces newlines in the values of a dictionary

    Args:
        dicts (list[dict[str, Any]]): List of dictionaries

    Returns:
        list[dict[str, Any]]: List of dictionaries with newlines replaced
    """
    new_dicts = deepcopy(dicts)
    for record in new_dicts:
        for key, value in record.items():
            if isinstance(value, str):
                record[key] = value.replace("\r\n", "\\r\\n")
    return new_dicts


def remove_unneeded_fields(
    records: list[dict[str, Any]], fields: list[str]
) -> list[dict[str, Any]]:
    """Removes unneeded fields from a list of records

    Args:
        records (list[dict[str,Any]]): List of records
        fields (list[str]): List of fields to remove

    Returns:
        list[dict[str,Any]]: List of records with the specified fields removed
    """
    new_records = deepcopy(records)
    for record in new_records:
        for field in fields:
            del record[field]

    return new_records


def filter_out_sobjects(sobjs: list[str]) -> list[str]:
    new_sobjs = deepcopy(sobjs)
    for u_sobj in UNSUPPORTED_SOBJS:
        if u_sobj in new_sobjs:
            new_sobjs.remove(u_sobj)
    return new_sobjs
