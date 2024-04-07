from settings import delete_account, crypt_passwords, decrypt_password,match_password, password_generator
from unittest.mock import patch, mock_open

def test_delete_account():
    mock_file = mock_open(read_data="Mail,Password\nuser1@example.com,pass1\nuser2@example.com,pass2")
    with patch("builtins.open", mock_file):
        assert delete_account("user1@example.com") == True


def test_crypt_decrypt():
    original_password = "my_password123"
    encrypted = crypt_passwords(original_password)
    assert original_password != encrypted
    assert decrypt_password(encrypted) == original_password


def test_match_password():
    assert match_password("password", "password") == True
    assert match_password("password", "different") == False

def test_password_generator():
    assert password_generator("Passw0rd!") == "Passw0rd!"
    assert password_generator("noSpecial123") == False
    assert password_generator("Short1!") == False