import pytest
from unittest.mock import MagicMock, patch, call
from file_writer import write_dict_to_csv, write_dict_to_file


@patch("csv.DictWriter")
@patch("file_writer.get_all_fields_for_object")
def test_write_dict_to_csv(mock_get_all_fields, mock_dict_writer):
    mock_session = MagicMock()
    mock_dicts = [{"name": "John", "age": 30}, {"name": "Alice", "age": 25}]
    mock_sobj = "my_object"
    mock_dict_writer.return_value = MagicMock()

    # Mock return values
    mock_get_all_fields.return_value = ["name", "age"]

    with patch("file_writer.open", create=True) as mock_open:
        # Call the function
        write_dict_to_csv(mock_session, mock_dicts, mock_sobj)

        # Assert the expected behavior
        mock_get_all_fields.assert_called_once_with(mock_session, mock_sobj)
        mock_open.assert_called_once_with("./csv/my_object.csv", "w", newline="")

        writer_mock = mock_dict_writer.return_value
        writer_mock.writeheader.assert_called_once()
        writer_mock.writerows.assert_called_once_with(mock_dicts)


def test_write_dict_to_file():
    mock_dicts = [{"name": "John", "age": 30}, {"name": "Alice", "age": 25}]
    mock_sobj = "my_object"

    with patch("file_writer.open", create=True) as mock_open:
        # Call the function
        write_dict_to_file(mock_dicts, mock_sobj)

        # Assert the expected behavior
        mock_open.assert_called_once_with("./failed/my_object.txt", "w")
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.write.assert_has_calls(
            [call(str(mock_dicts[0]) + "\n"), call(str(mock_dicts[1]) + "\n")]
        )
