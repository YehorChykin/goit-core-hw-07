from collections import UserDict
from datetime import datetime, timedelta
import os

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

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # def delete_phone(self, phone):
    #     for p in self.phones:
    #         if p.value == phone:
    #             self.phones.remove(p)
    #             return

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def add_birthday(self, birthday):
        if self.birthday is None:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Birthday already exists for this contact")

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday}" if self.birthday else f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]

    def find_record(self, name):
        return self.data.get(name)

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find_record(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added"
    if phone:
        record.add_phone(phone)
    return message

def change(args, book: AddressBook):
    name, old_number, new_number, *_ = args
    record = book.find_record(name)
    record.edit_phone(old_number, new_number)
    message = "Contact changed"
    return message

def find_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find_record(name)
    if record:
        if record.phones:
            return f"Phones of {name}: {', '.join(str(phone) for phone in record.phones)}"
        else:
            return f"No phone found for {name}."
    else:
        return f"No contact found for {name}."

def all(book:AddressBook):
    for name, record in book.data.items():
        print(record)

def add_birthday(args, book: AddressBook):
    if len(args) != 2:
        return "Invalid number of arguments. Usage: add-birthday [name] [birthday]"
    name, birthday = args
    record = book.find_record(name)
    if record:
        try:
            record.add_birthday(birthday)
            return f"Birthday added for {name}."
        except ValueError as e:
            return str(e)
    else:
        return f"No contact found for {name}."

def show_birthday(args, book: AddressBook):
    if len(args) != 1:
        return "Invalid number of arguments. Usage: show-birthday [name]"
    name = args[0]
    record = book.find_record(name)
    if record:
        if record.birthday:
            return f"{name}'s birthday: {record.birthday.value}"
        else:
            return f"No birthday found for {name}."
    else:
        return f"No contact found for {name}."
    
def birthday(book: AddressBook):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    upcoming_birthdays = []
    for record in book.data.values():
        if record.birthday:
            birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            birthday_date = birthday_date.replace(year=datetime.now().year)
            difference_days = (birthday_date - today).days
            if difference_days <= 7 and difference_days >= 0:
                if birthday_date.weekday() >= 5:
                    days_until_monday = 7 - birthday_date.weekday()
                    birthday_date += timedelta(days=days_until_monday)
                upcoming_birthdays.append({"name": record.name.value, "Congratulatinons_day": birthday_date.strftime("%Y.%m.%d")})
    return upcoming_birthdays

def main():
    book = AddressBook()   
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change(args, book))
        elif command == "phone":
            print(find_phone(args,book))
        elif command == "all":
            all(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthday(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()