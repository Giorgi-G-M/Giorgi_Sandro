import csv
import tabulate


def contact_main(id):
    if not get_user_contacts(id):
        print("You have no contacts yet. Let's add a contact.")
        add_contact_loop(id)
    try:
        with open("contact.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            is_empty = len(list(reader)) == 0
    except FileNotFoundError:
        is_empty = True

    if is_empty:
        print("You have no contacts yet. Let's add a contact.")
        add_contact_loop(id)

    while True:
        print("\n1. Add New Contact")
        print("2. Modify Contact")
        print("3. Search Contacts by Alphabet")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_contact_loop(id)
        elif choice == "2":
            modify_contact(id)
        elif choice == "3":
            search_contacts(id)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


def get_user_contacts(user_id):
    try:
        with open("contact.csv", "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader if row["UserId"] == user_id]
    except FileNotFoundError:
        return []
def add_new_contact(user_id, name, surname, phonenumber, mail):
    try:
        with open("contact.csv", "a", newline="") as csvfile:
            fieldnames = ["Id", "UserId", "Name", "Surname", "Phonenumber", "Mail"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            with open("contact.csv", "r") as csvfile_read:
                reader = csv.DictReader(csvfile_read)
                next_id = max([int(row["Id"]) for row in reader if row["Id"].isdigit()], default=0) + 1

            writer.writerow(
                {"Id": next_id,"UserId": user_id, "Name": name, "Surname": surname, "Phonenumber": phonenumber, "Mail": mail}
            )

        print("Contact added successfully.")
        return True
    except IOError:
        print("Error: Unable to write to file.")
        return False
    except Exception as e:
        print("Error:", e)
        return False
    

def modify_contact(user_id):
    user_contacts = get_user_contacts(user_id)
    if not user_contacts:
        print("You have no contacts yet. Please add a contact first.")
        return False

    print("Here are your contacts:")
    with open("contact.csv", "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        headers = reader.fieldnames

        for row in reader:
            if row["UserId"] == user_id:
                data.append([row[header] for header in headers])

        print(tabulate.tabulate(data, headers=headers, tablefmt="grid"))

    while True:
        contact_id = input("Enter the ID of the contact you want to modify or 'D' to delete: ")
        if contact_id.lower() == "d":
            delete_contact(user_id)
            return True

        try:
            contact_id = int(contact_id)
            if contact_id in [int(contact["Id"]) for contact in user_contacts]:
                # Find the contact to modify
                for contact in user_contacts:
                    if int(contact["Id"]) == contact_id:
                        print("What information would you like to change for contact with ID", contact_id, "?")
                        print("1. Name")
                        print("2. Surname")
                        print("3. Phone number")
                        print("4. Email")
                        print("5. Back")
                        print("6. Delete contact")
                        choice = input("Enter your choice (1/2/3/4/5/6): ")

                        if choice == "1":
                            new_name = input("Enter the new name: ")
                            contact["Name"] = new_name
                            print("Name updated successfully.")
                        elif choice == "2":
                            new_surname = input("Enter the new surname: ")
                            contact["Surname"] = new_surname
                            print("Surname updated successfully.")
                        elif choice == "3":
                            new_phone = input("Enter the new phone number: ")
                            contact["Phonenumber"] = new_phone
                            print("Phone number updated successfully.")
                        elif choice == "4":
                            new_email = input("Enter the new email: ")
                            contact["Mail"] = new_email
                            print("Email updated successfully.")
                        elif choice == "5":
                            return False  # User chose to go back
                        elif choice == "6":
                            delete_contact(user_id)  # Call the delete function
                            return True  # Deleted successfully
                        else:
                            print("Invalid choice.")

                        # Update the CSV file with the modified contact
                        with open("contact.csv", "w", newline="") as csvfile:
                            fieldnames = ["Id","UserId", "Name", "Surname", "Phonenumber", "Mail"]
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(user_contacts)

                        return True  # Modified successfully
            else:
                print("Invalid contact ID. Please enter a valid ID from the list.")
        except ValueError:
            print("Invalid input. Please enter a valid contact ID.")


def delete_contact(user_id):
    user_contacts = get_user_contacts(user_id)
    if not user_contacts:
        print("You have no contacts yet. Please add a contact first.")
        return False

    print("Here are your contacts:")
    print(tabulate.tabulate(user_contacts, headers="keys"))

    contact_id = input("Enter the ID of the contact you want to delete: ")
    for contact in user_contacts:
        if contact["Id"] == contact_id:
            user_contacts.remove(contact)

            # Update the CSV file with the modified contact list
            with open("contact.csv", "w", newline="") as csvfile:
                fieldnames = ["Id","UserId", "Name", "Surname", "Phonenumber", "Mail"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(user_contacts)

            print("Contact deleted successfully.")
            return True

    print("Invalid contact ID.")
    return False


def search_contacts(user_id):
    user_contacts = get_user_contacts(user_id)
    if not user_contacts:
        print("You have no contacts yet. Please add a contact first.")
        return False

    print("Here are your contacts:")
    print(tabulate.tabulate(user_contacts, headers="keys"))

    search_key = input("Enter the alphabet to search contacts (A-Z): ").lower()
    filtered_contacts = [
        contact for contact in user_contacts if contact["Name"].startswith(search_key) or contact["Surname"].startswith(search_key)
    ]
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
    contact_main()
