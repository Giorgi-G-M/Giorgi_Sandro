import re
import os
import string
import tabulate
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

def main():

    # Check if there are any users registered
    with open("results.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        if not any(reader):
            registration_form()
    

    while True:
        if LogIn():
            print("\n1. Weather application\n2. Settings\n3. Contact information")
            user_choice = input("Choose your application: ")
            if user_choice == "Weather application" or user_choice == "1":
                pass
            elif user_choice == "Settings" or user_choice == "2":
                while True:
                    print("1. Change Password\n2. Delete Account\n3. Change personal information")
                    settings_choice = input("Choose your action: ").lower()
                    if settings_choice == "Change Password" or settings_choice == "1":
                        password_changer()
                    elif settings_choice == "back":
                        break  # Go back to main menu
                    elif settings_choice == "Delete Account" or settings_choice == "2":
                        if delete_account():
                            break  # Account deleted, break out of the loop
                    elif settings_choice == "back":
                        break  # Go back to main menu
                    elif settings_choice == "Change personal infomration" or settings_choice == "3":
                        personal_info_changer()
                    elif settings_choice == "back":
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif user_choice == "Contact information" or user_choice == "3":
                user_id = input("Enter your user ID: ")

                # Check if the contact CSV file is empty
                with open("contact.csv", "r") as csvfile:
                    reader = csv.reader(csvfile)
                    is_empty = len(list(reader)) == 0

                if is_empty:
                    print("You have no contacts yet. Let's add a contact.")
                    add_contact_loop(user_id)

                while True:
                    print("\n1. Add New Contact")
                    print("2. Modify Contact")
                    print("3. Search Contacts by Alphabet")
                    print("4. Exit")

                    choice = input("Enter your choice: ")

                    if choice == "1":
                        add_contact_loop(user_id)
                    elif choice == "2":
                        modify_contact(user_id)
                    elif choice == "3":
                        search_contacts(user_id)
                    elif choice == "4":
                        print("Exiting...")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            break
        else:
            print("Invalid email address or password. Please try again or register.")
            user = input("Are you registered on our platform? Please enter one of them. Yes/No: ").lower()
            if user == "no":
                registration_form()

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
                        return True
        
        print("Invalid email address or password. Please try again or register.")
        user = input("Are you registered on our platform? Please enter Yes/No: ").lower()
        if user != "yes":
            return registration_form()

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
                return LogIn()
            else:
                print("Error retrieving user ID.") 
            break
        else:
            print("Invalid email address or password\nPassword must be at least 8 characters long.\n"
                  "contain at least one digit, and contain at least one special character.")

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


# Function to add a new contact to the CSV file
def add_new_contact(user_id, name, surname, phonenumber, mail):
    with open('contact.csv', 'a', newline='') as csvfile:
        fieldnames = ['Id', 'Name', 'Surname', 'Phonenumber', 'Mail']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Find the maximum ID in the CSV file
        with open('contact.csv', 'r') as csvfile_read:
            reader = csv.DictReader(csvfile_read)
            ids = [int(row['Id']) for row in reader if row['Id'].isdigit()]
            next_id = max(ids) + 1 if ids else 1

        # Write the new contact to the CSV file
        writer.writerow({'Id': next_id, 'Name': name, 'Surname': surname, 'Phonenumber': phonenumber, 'Mail': mail})

    print("Contact added successfully.")
    return True

# Function to retrieve user's contacts from the CSV file
def get_user_contacts(user_id):
    user_contacts = []
    with open("contact.csv", "r", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Id'] == user_id:
                user_contacts.append(row)
    return user_contacts

# Function to modify an existing contact
def modify_contact(user_id):
    user_contacts = get_user_contacts(user_id)
    if not user_contacts:
        print("You have no contacts yet. Please add a contact first.")
        return False

    print("Here are your contacts:")
    print(tabulate.tabulate(user_contacts, headers="keys"))

    contact_id = input("Enter the ID of the contact you want to modify: ")
    for contact in user_contacts:
        if contact['Id'] == user_id and contact['Id'] == contact_id:
            print("What information would you like to change?")
            print("1. Name")
            print("2. Surname")
            print("3. Phone number")
            print("4. Email")
            print("5. Back")
            choice = input("Enter your choice (1/2/3/4/5): ")

            if choice == "1":
                new_name = input("Enter the new name: ")
                contact['Name'] = new_name
                print("Name updated successfully.")
            elif choice == "2":
                new_surname = input("Enter the new surname: ")
                contact['Surname'] = new_surname
                print("Surname updated successfully.")
            elif choice == "3":
                new_phone = input("Enter the new phone number: ")
                contact['Phonenumber'] = new_phone
                print("Phone number updated successfully.")
            elif choice == "4":
                new_email = input("Enter the new email: ")
                contact['Mail'] = new_email
                print("Email updated successfully.")
            elif choice == "5":
                return False  # User chose to go back
            else:
                print("Invalid choice.")

            # Update the CSV file with the modified contact
            with open("contact.csv", "w", newline='') as csvfile:
                fieldnames = ['Id', 'Name', 'Surname', 'Phonenumber', 'Mail']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(user_contacts)

            return True  # Modified successfully

    print("Invalid contact ID.")
    return False

# Function to search for contacts by alphabet
def search_contacts(user_id):
    user_contacts = get_user_contacts(user_id)
    if not user_contacts:
        print("You have no contacts yet. Please add a contact first.")
        return False

    print("Here are your contacts:")
    print(tabulate.tabulate(user_contacts, headers="keys"))

    search_key = input("Enter the alphabet to search contacts (A-Z): ").lower()
    filtered_contacts = [contact for contact in user_contacts if contact['Name'].startswith(search_key) or contact['Surname'].startswith(search_key)]
    if filtered_contacts:
        print("Filtered contacts:")
        print(tabulate.tabulate(filtered_contacts, headers="keys"))
    else:
        print("No contacts found for the entered alphabet.")


def add_contact_loop(user_id):
    while True:
        name = input("Enter name: ")
        surname = input("Enter surname: ")
        
        # Check if name and surname contain only alphabetic characters
        if not name.isalpha() or not surname.isalpha():
            print("Name and surname should only contain alphabetic characters.")
            continue

        phonenumber = input("Enter phone number: ")
        
        # Check if phone number contains only digits
        if not phonenumber.isdigit():
            print("Phone number should only contain digits.")
            continue

        mail = input("Enter email: ")

        if add_new_contact(user_id, name, surname, phonenumber, mail):
            break  # Exit the loop if the contact is successfully added


if __name__ == "__main__":
    main()
