import os
import pytest
from unittest.mock import MagicMock
from setup import setup_local_env


def test_setup_local_env():
    # Mock os.path.exists to return False
    os.path.exists = MagicMock(return_value=False)

    # Track the calls to os.makedirs
    makedirs_calls = []

    def mock_makedirs(path):
        makedirs_calls.append(path)

    # Patch os.makedirs with the mock function
    os.makedirs = MagicMock(side_effect=mock_makedirs)

    # Call the function
    setup_local_env()

    # Assert that os.makedirs was called with the correct paths
    assert len(makedirs_calls) == 2
    assert makedirs_calls[0].endswith("/csv")
    assert makedirs_calls[1].endswith("./failed")

    # Restore the original functions
    os.path.exists = MagicMock()
    os.makedirs = MagicMock()
