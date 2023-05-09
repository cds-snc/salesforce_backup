import pytest
import data as d


def test_build_query_all_records():
    assert (
        d.build_query_all_records("Account", 100, 0)
        == "SELECT FIELDS(ALL) FROM Account ORDER BY Id LIMIT 100 OFFSET 0"
    )
