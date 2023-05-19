import pytest
import reader as r


def test_build_query_all_records():
    assert (
        r.build_query_all_records("Account", 100, 0)
        == "SELECT FIELDS(ALL) FROM Account ORDER BY Id LIMIT 100 OFFSET 0"
    )
