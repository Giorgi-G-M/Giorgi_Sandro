import pytest
from unittest.mock import patch, mock_open
from contact import add_new_contact, get_user_contacts

def test_add_new_contact_success():
    assert add_new_contact("1", "Test", "User", "1234567890", "test@example.com") == True

def test_get_user_contacts_empty_for_non_existent_user():
    assert get_user_contacts("non_existent_user") == []

def test_get_user_contacts_returns_list():
    user_id = "some_user_id"
    result = get_user_contacts(user_id)
    assert isinstance(result, list)


def test_add_new_contact_with_mock():
    mock_file = mock_open()
    with patch('builtins.open', mock_file):
        assert add_new_contact("1", "John", "Doe", "123456789", "john@example.com") == True
        mock_file().write.assert_called_once()
