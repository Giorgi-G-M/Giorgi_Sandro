import pytest
from register import (
    validate_email,
    password_generator,
    match_password,
    crypt_passwords,
    decrypt_password,
)

# Test validate_email function
def test_validate_email_valid():
    assert validate_email("test@example.com") == True

def test_validate_email_invalid():
    assert validate_email("invalid_email") == False

# Test password_generator function
def test_password_generator_valid():
    assert password_generator("Test@123") == "Test@123"

def test_password_generator_invalid():
    assert password_generator("weakpassword") == False

# Test match_password function
def test_match_password_match():
    assert match_password("password", "password") == True

def test_match_password_mismatch():
    assert match_password("password", "different_password") == False

# Test crypt_passwords and decrypt_password functions
def test_crypt_decrypt_password():
    password = "Test@123"
    encrypted_password = crypt_passwords(password)
    decrypted_password = decrypt_password(encrypted_password)
    assert decrypted_password == password

# Additional test cases for decrypt_password function
def test_decrypt_password_invalid_input():
    with pytest.raises(Exception):
        decrypt_password("invalid_input")

def test_decrypt_password_empty_input():
    with pytest.raises(Exception):
        decrypt_password("")
