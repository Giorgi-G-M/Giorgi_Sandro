import re
import os
import string
import tabulate
import csv
import getpass
import string
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from enterer import main
load_dotenv()

# Global variables for decrypt and encrypt passwords
SECRET_KEY = os.getenv("SECRET_KEY")
assert SECRET_KEY
FERNET = Fernet(SECRET_KEY)

def register_main():
    # Check if there are any users registered
    with open("results.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        if not any(reader):
            registration_form()
    
    while True:
        try:
            user = input("Are you registered on our platform? Please enter one of them. Yes/No: ").lower()
            if user == "no":
                registration_form()
            elif user == "yes":
                return LogIn()
                break
            else:
                print("Invalid input")
        except ValueError:
            continue

# Email validation by regex
def validate_email(user_mail):
    regex = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-z]+(?:[a-z-]*[a-z])?(?:\.[a-z]+(?:[a-z-]*[a-z])?)*$"
    return re.match(regex, user_mail) is not None

# Password validation
def password_generator(user_password):
    if len(user_password) >= 8 and any(char in string.punctuation for char in user_password) and any(char.isdigit() for char in user_password):
        return user_password
    else:
        return False

# Password confirmation
def match_password(password, user_match_password):
    return password == user_match_password

# Encryption passwords
def crypt_passwords(password):
    load_dotenv()
    return FERNET.encrypt(password.encode()).decode()

# Decrypt passwords
def decrypt_password(encrypted_password):
    return FERNET.decrypt(encrypted_password).decode()

# Function to add a new user to the CSV file
def add_new_user(user_name, user_surname, user_mail, encrypted_password):
    with open('results.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        ids = [int(row['Id']) for row in reader if row['Id'].isdigit()]
        next_id = max(ids) + 1 if ids else 1
    with open('results.csv', 'a', newline='') as csvfile:
        fieldnames = ['Id', 'Username', 'Surname', 'Mail', 'Password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvfile.seek(0, 2)
        is_empty = csvfile.tell() == 0
        if is_empty:
            writer.writeheader()
        writer.writerow({'Id': next_id, 'Username': user_name, 'Surname': user_surname, 'Mail': user_mail, 'Password': encrypted_password})
    return True

# Function to write user data to the CSV file
def mail_password_csv(user_mail, decrypted_password):
    with open("results.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        ids = [int(row['Id']) for row in reader if row['Id'].isdigit()]
        next_id = max(ids) + 1 if ids else 1
    with open("results.csv", 'a', newline='') as csvfile:
        fieldnames = ['Id', 'Mail', 'Password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvfile.seek(0, 2)
        is_empty = csvfile.tell() == 0
        if is_empty:
            writer.writeheader()
        writer.writerow({'Id': next_id, 'Mail': user_mail, 'Password': decrypted_password})
    return True

# Function for user login
def LogIn():
    while True:
        user_mail = input("Input your email here: ").lower()
        user_password = getpass.getpass("Enter your password: ").strip()
        
        try:
            with open("results.csv", 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['Mail'] == user_mail:
                        decrypted_password = decrypt_password(row['Password'])
                        if decrypted_password == user_password:
                            print("Login successful!\n")
                            # Print user information for the logged-in user
                            user_info = [row["Id"], row["Username"], row["Surname"], row["Mail"]]
                            print(tabulate.tabulate([user_info], headers=["ID", "Username", "Surname", "Email"]))
                            return True,user_info[0]
                else:
                    print("Invalid email address or password. Please try again or register.")
                    user = input("Are you registered on our platform? Please enter Yes/No: ").lower()
                    if user != "yes":
                        return registration_form()
        except FileNotFoundError:
            print("Error: File 'results.csv' not found.")
            return False

# Function for user registration
def registration_form():
    user_name = input("Please enter your name: ")
    user_surname = input("Enter your surname: ")
    
    while True:
        user_mail = input("Input your email here: ").lower()
        # Check if email already exists
        with open("results.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Mail'] == user_mail:
                    print("Email already registered. Please choose a different email.")
                    break
            else:
                break  # If no matching email found, break out of the loop

    while True:
        user_password = getpass.getpass("Enter your password: ").strip()
        user_match_password = getpass.getpass("Please confirm your password: ").strip()
        if validate_email(user_mail) and match_password(user_password, user_match_password) and password_generator(user_password):
            # Add the new user to the CSV file
            encrypted_password = crypt_passwords(user_password)
            add_new_user(user_name, user_surname, user_mail, encrypted_password)
            
            # Retrieve the user ID
            with open("results.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                user_id = None
                for row in reader:
                    if row['Mail'] == user_mail:
                        user_id = row['Id']
                        break
            
            # Print registration success message with user ID
            if user_id:
                print("\nCongratulations! You have registered successfully!")
                print(f"\nPlease remember your Number ID '{user_id}'. If you ever forget your password, you will need it to restore your account.")
                return True
            else:
                print("Error retrieving user ID.") 
            break
        else:
            print("Invalid email address or password\nPassword must be at least 8 characters long.\n"
                  "contain at least one digit, and contain at least one special character.")


# Function to update password in the CSV file
def forget_password():
    user_email = input("Enter your Email: ")
    user_name = input("Enter your name: ")
    user_surname = input("Enter your surname: ")
    user_id = input("Enter your Id: ")

    data_results = []

    with open("results.csv", "r", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames_results = reader.fieldnames

        for row in reader:
            if (user_email == row["Mail"] and user_name == row["Username"] 
                and user_surname == row["Surname"] and user_id == row["Id"]):
                user_password = getpass.getpass("Please input your new password: ")
                if password_generator(user_password):
                    password_confirm = getpass.getpass("Please confirm your Password: ")
                    if user_password != password_confirm:
                        print("Password doesn't match")
                    else:
                        # Update the password in the data
                        row['Password'] = crypt_passwords(user_password)
                        data_results.append(row)
                else:
                    print("Invalid password. Password must be at least 8 characters long, "
                          "contain at least one digit, and contain at least one special character.")
                    return False

    if data_results:
        # Write the updated data back to the CSV file
        with open("results.csv", "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_results)
            writer.writeheader()
            writer.writerows(data_results)
        print("Password changed successfully.")
        return True
    else:
        print("User not found.")
        return False
    
if __name__ == "__main__":
    register_main()
