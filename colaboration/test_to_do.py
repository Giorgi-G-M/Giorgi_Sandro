import pytest
from unittest.mock import mock_open, patch
from to_do import write_data

def test_write_data():
    mock_data = ["Task 1", "Task 2"]
    m = mock_open()
    with patch("builtins.open", m, create=True):
        write_data(mock_data)
    m.assert_called_once_with("task.txt", "w")
    handle = m()
    handle.write.assert_any_call("Task 1\n")
    handle.write.assert_any_call("Task 2\n")


@patch('builtins.open', new_callable=mock_open, read_data="Task 1\nTask 2\n")
def test_get_data(mock_file):
    from to_do import get_data
    data = get_data()
    assert data == ["Task 1", "Task 2"]


@patch('to_do.get_data', return_value=["Task 1", "Task 2", "Task 3"])
@patch('to_do.write_data')
def test_remove_data(mock_write_data, mock_get_data):
    from to_do import remove_data
    remove_data(2)
    mock_write_data.assert_called_once_with(["Task 1", "Task 3"])
