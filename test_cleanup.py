import cleanup as c


def test_remove_unneeded_fields():
    records = [
        {
            "Id": 1,
            "attributes": {"type": "Account", "url": "http://foo.bar"},
            "Name": "Test",
        }
    ]
    assert c.remove_unneeded_fields(records, ["attributes"]) == [
        {"Id": 1, "Name": "Test"}
    ]


def test_replace_newlines_in_dict_values():
    assert c.replace_newlines_in_dict_values([{"Id": 1, "Name": "Test\r\nTest"}]) == [
        {"Id": 1, "Name": "Test\\r\\nTest"}
    ]


def test_filter_out_sobjects_removes_objs():
    sobjs = [
        "Foo",
        "Bar",
        "Scorecard",
        "ScorecardAssociation",
        "ScorecardMetric",
        "UserExternalCredential",
        "WebCartDocument",
    ]
    assert c.filter_out_sobjects(sobjs) == ["Foo", "Bar"]


def test_filter_out_sobjects_deep_copies():
    sobjs = [
        "Foo",
        "Bar",
        "Scorecard",
        "ScorecardAssociation",
        "ScorecardMetric",
        "UserExternalCredential",
        "WebCartDocument",
    ]
    c.filter_out_sobjects(sobjs)
    assert [
        "Foo",
        "Bar",
        "Scorecard",
        "ScorecardAssociation",
        "ScorecardMetric",
        "UserExternalCredential",
        "WebCartDocument",
    ] == sobjs


def test_filter_out_sobjects_if_not_all_there():
    sobjs = ["Foo", "Bar", "Scorecard"]
    assert ["Foo", "Bar"] == c.filter_out_sobjects(sobjs)
