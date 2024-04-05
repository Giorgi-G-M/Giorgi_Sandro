# # import bcrypt
# from register import cipher
# password = b"my"
# # Generate a salt
# salt = bcrypt.gensalt()
# # Hash the password
# hashed_password = bcrypt.hashpw(password, salt)
# print(hashed_password)

from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
# # Create a cipher using the key
cipher = Fernet(key)

# # Password to encrypt
# password = b"secret_password"

# # Encrypt the password
# encrypted_password = cipher.encrypt(password)

# print("Encrypted password:", encrypted_password)

# # Decrypt the password
# decrypted_password = cipher.decrypt(encrypted_password)

# print("Decrypted password:", decrypted_password.decode())


    # regex = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-z]+(?:[a-z-]*[a-z])?(?:\.[a-z]+(?:[a-z-]*[a-z])?)*$"
    # return re.match(regex, user_mail) is not None



# import csv
# import sys
# import os
# from contextlib import ExitStack

# FIELD_NAMES = ['id', 'data_column_1', 'data_column_2']

# def main(args):
#     input_path, output_dir = args
#     writers = {}
#     with ExitStack() as stack:
#         input_file = stack.enter_context(open(input_path, 'rt'))
#         for line in input_file:
#             cells = line.split()
#             row_id = cells[0]
#             if row_id not in writers:
#                 writers[row_id] = get_writer(output_dir, row_id, stack)
#             writers[row_id].writerow(dict(zip(FIELD_NAMES, cells)))

# def get_writer(output_dir, row_id, stack):
#     path = os.path.join(output_dir, row_id + '.csv')
#     file = open(path, 'w', newline = '', encoding = 'utf-8')
#     stack.enter_context(file)
#     writer = csv.DictWriter(file, fieldnames = FIELD_NAMES)
#     writer.writeheader()
#     return writer

# if __name__ == '__main__':
#     main(sys.argv[1:])


# def crypt_passwords(password):
#     return cipher.encrypt(password.encode())

# # Decrypt passwords
# def decrypt_password():
#     return cipher.decrypt(b'gAAAAABmDxC4AY7P4oFXI59Y98IGpNgVL6dDfPtWKqModLHIHxf82-CwIcg1pWQj1WwTuDsakP3RUVudFiFjaEDBzd0y2e28TA==')

# print(decrypt_password())

# print(crypt_passwords("Girogi"))


# from cryptography.fernet import Fernet
# key = Fernet.generate_key()
# f = Fernet(key)
# token = f.encrypt(b"my deep dark secret")
# print(f.decrypt(token))

# import base64
# import os
# from cryptography.fernet import Fernet
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# password = b"password"
# salt = os.urandom(16)
# kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=salt,
#     iterations=480000,
# )
# key = base64.urlsafe_b64encode(kdf.derive(password))
# f = Fernet(key)
# token = f.encrypt("Secret message!")
# print(token)
# print(f.decrypt(token))
# 'Secret message!'

# Import the necessary modules

# from cryptography.fernet import Fernet
# key = Fernet.generate_key()
# f = Fernet(key)
# token = f.encrypt(b"my deep dark secret")
# token
# b'...'
# f.decrypt(token)
# import hashlib

# password = input("Password: ")
# password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
# print(f"Password Hash: {password_hash}")

# import os
# import sys

# from cryptography.fernet import Fernet
# from dotenv import load_dotenv

# load_dotenv()

# SECRET_KEY = os.getenv("SECRET_KEY")
# assert SECRET_KEY
# FERNET = Fernet(SECRET_KEY)

# if len(sys.argv) > 1 and sys.argv[1] == "decrypt":
#     with open("pw.txt") as f:
#         stored_password = f.read()

#     stored_dec_password = FERNET.decrypt(stored_password).decode()
#     print(f"Decrypted Password: {stored_dec_password}")
# else:
#     new_password = input("New Password: ")
#     new_enc_password = FERNET.encrypt(new_password.encode()).decode()

#     with open("pw.txt", "w") as f:
#         f.write(new_enc_password)

#     print(f"Encrypted Password Stored: {new_enc_password}")