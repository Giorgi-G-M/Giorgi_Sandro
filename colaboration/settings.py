import os
import string
import csv
import getpass
import string
from cryptography.fernet import Fernet
from dotenv import load_dotenv
load_dotenv()
# Global variables for decrypt and encrypt passwords
SECRET_KEY = os.getenv("SECRET_KEY")
assert SECRET_KEY
FERNET = Fernet(SECRET_KEY)


def settings_main():
    print("1. Delete account\n2. Change personal infromation\n 3. Change password\n4. Back to the main")
    while True:
        user = input("Choose your applictaion: ")
        if user.isdigit():
            if user == "1":
                delete_account()
            elif user == "2":
                personal_info_changer()
            elif user == "3":
                password_changer()
            else:
                continue



def password_generator(user_password):
    if len(user_password) >= 8 and any(char in string.punctuation for char in user_password) and any(char.isdigit() for char in user_password):
        return user_password
    else:
        return False


def match_password(password, user_match_password):
    return password == user_match_password

# Encryption passwords
def crypt_passwords(password):
    load_dotenv()
    return FERNET.encrypt(password.encode()).decode()

# Decrypt passwords
def decrypt_password(encrypted_password):
    return FERNET.decrypt(encrypted_password).decode()


# Function for deleting an account
def delete_account():
    while True:
        user_mail = input("Enter your email to confirm account deletion (or type 'back' to return to previous menu): ").lower()
        if user_mail == 'back':
            return False  # User chose to go back
        found = False
        with open("results.csv", "r", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Mail'] == user_mail:
                    found = True
                    break
        if found:
            # Proceed with account deletion
            data_results = []
            with open("results.csv", "r", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                fieldnames_results = reader.fieldnames
                for row in reader:
                    if row['Mail'] != user_mail:
                        data_results.append(row)
            with open("results.csv", "w", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames_results)
                writer.writeheader()
                writer.writerows(data_results)

            print(f"Account with email {user_mail} has been successfully deleted.")
            return True  # Deletion successful
        else:
            print("Invalid email. Please try again.")

#This function is supposted to change Name/Surname/Email
def personal_info_changer():
    user_mail = input("Enter your current email: ").lower()

    # Read the existing user data
    data = []
    with open("results.csv", "r", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        for row in reader:
            if row['Mail'] == user_mail:
                while True:
                    print("What information would you like to change?")
                    print("1. Name")
                    print("2. Surname")
                    print("3. Email")
                    print("4. Back")
                    choice = input("Enter your choice (1/2/3/4): ")

                    if choice == "1":
                        new_name = input("Enter your new name: ")
                        row['Username'] = new_name
                        print("Name updated successfully.")
                    elif choice == "2":
                        new_surname = input("Enter your new surname: ")
                        row['Surname'] = new_surname
                        print("Surname updated successfully.")
                    elif choice == "3":
                        while True:
                            new_email = input("Enter your new email: ").lower()
                            if new_email == user_mail:
                                print("New email cannot be the same as the current email.")
                            elif any(row['Mail'] == new_email for row in data):
                                print("Email already exists. Please choose a different email.")
                            else:
                                row['Mail'] = new_email
                                print("Email updated successfully.")
                                break
                    elif choice == "4":
                        return False  # User chose to go back
                    else:
                        print("Invalid choice.")
                    
                    # Append the updated row to the data list
                    data.append(row)

                    # Write the updated data back to the CSV file
                    with open("results.csv", "w", newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(data)

                    return True
            else:
                data.append(row)


    # Write the updated data back to the CSV file
    with open("results.csv", "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return True

# Function for changing password from application's settings
def password_changer():
    while True:
        user_mail = input("Enter your email: ").lower()
        old_password = getpass.getpass("Enter your current password: ").strip()
        new_password = getpass.getpass("Enter your new password: ").strip()
        confirm_password = getpass.getpass("Confirm your new password: ").strip()

        if new_password != confirm_password:
            print("New passwords do not match. Please try again.")
            continue

        # Decrypt the new password
        encrypted_new_password = crypt_passwords(new_password)

        # Read the existing user data
        data = []
        with open("results.csv", "r", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['Mail'] == user_mail and decrypt_password(row['Password']) == old_password:
                    row['Password'] = encrypted_new_password
                data.append(row)

        # Write the updated data back to the CSV file
        with open("results.csv", "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print("Password changed successfully.")
        return True


if __name__ == "__main__":
    settings_main()