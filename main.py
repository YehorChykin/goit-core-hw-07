from main1 import AddressBook, Record, Birthday
from datetime import datetime, timedelta

contacts_file_path = r"D:\Projects\start_python\modul_7\HW_7\contacts.txt"

print("Hi, can I help you?")

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter a valid command."
        except ValueError:
            return "Invalid input. Try again."
        except IndexError:
            return "Invalid input format. Please try again."

    return inner

@input_error
def add_contact(name, phone_number):
    try:
        if not phone_number.startswith('+') and not phone_number.isdigit():
            raise ValueError("Phone number should start with '+' or consist of digits only")
        elif not phone_number[1:].isdigit():
            raise ValueError("Invalid phone number format")
            
        with open(contacts_file_path, 'a') as file:
            file.write(f"{name},{phone_number}\n")
        print("Contact added.")
        return "Contact added."
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"


@input_error
def change_contact(name, new_phone_number):
    try:
        with open(contacts_file_path, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            contact_name, _ = line.strip().split(',')
            if contact_name == name:
                lines[i] = f"{name},{new_phone_number}\n"
                break
        with open(contacts_file_path, 'w') as file:
            file.writelines(lines)
        print("Contact updated.")
        return "Contact updated."
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

@input_error
def show_phone(name):
    try:
        with open(contacts_file_path, 'r') as file:
            for line in file:
                contact_name, phone_number = line.strip().split(',')
                if contact_name == name:
                    print(f"Name: {name}, Number: {phone_number}")
                    return f"Name: {name}, Number: {phone_number}"
            else:
                print(f"No contact found for {name}")
                return f"No contact found for {name}"
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

@input_error
def show_all():
    try:
        with open(contacts_file_path, 'r') as file:
            contacts = file.readlines()
            for contact in contacts:
                name, phone_number = contact.strip().split(',')
                print(f"Name: {name}, Number: {phone_number}")
            return contacts
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
    
@input_error
def add_birthday(args, book):
    if len(args) != 2:
        return "Invalid number of arguments. Usage: add-birthday [name] [birthday]"
    name = args[0]
    birthday = args[1]
    try:
        book.find_record(name).add_birthday(birthday)
        return f"Birthday added for {name}."
    except ValueError as e:
        return str(e)

@input_error
def show_birthday(args, book):
    if len(args) != 1:
        return "Invalid number of arguments. Usage: show-birthday [name]"
    name = args[0]
    record = book.find_record(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value}"
    else:
        return f"No birthday found for {name}."

@input_error
def birthdays(args, book):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    upcoming_birthdays = []
    for record in book.data.values():
        if record.birthday:
            birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            if today <= birthday_date < next_week:
                upcoming_birthdays.append(record.name.value)
    if upcoming_birthdays:
        return "Users to congratulate next week: " + ", ".join(upcoming_birthdays)
    else:
        return "No upcoming birthdays next week"

def parse_input(user_input):
    parts = user_input.lower().split()
    command = parts[0]
    arguments = parts[1:]
    return command, arguments

def main():
    book = AddressBook()

    while True:
        user_input = input("Enter a command (hello/close/exit/add/change/show_phone/all/add-birthday/show-birthday/birthdays): ")
        command, arguments = parse_input(user_input)

        if command == "hello":
            print("How can I help you?")
        elif "exit" in command or "close" in command:
            print("Goodbye!")
            break
        elif command == "add":
            name = input("Enter your contact name: ").strip()
            phone_number = input("Enter your contact number: ").strip()
            book.add_record(Record(name))
            book.data[name].add_phone(phone_number)
            print("Contact added.")
        elif command == "change":
            name = input("Enter the contact name: ").strip()
            new_phone_number = input("Enter the new phone number: ").strip()
            book.find_record(name).edit_phone(book.find_record(name).phones[0].value, new_phone_number)
            print("Contact updated.")
        elif command == "show_phone":
            name = input("Enter the contact name: ").strip()
            phone_number = book.find_record(name).phones[0].value
            print(f"Name: {name}, Number: {phone_number}")
        elif command == "all":
            print("All contacts:")
            for record in book.data.values():
                phones = '; '.join([phone.value for phone in record.phones])
                print(f"Name: {record.name.value}, Phones: {phones}")
        elif command == "add-birthday":
            result = add_birthday(arguments, book)
            print(result)
        elif command == "show-birthday":
            result = show_birthday(arguments, book)
            print(result)
        elif command == "birthdays":
            result = birthdays(arguments, book)
            print(result)
        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()