from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    @staticmethod
    def validate_phone(phone):
        if not phone.startswith('+'):
            return False
        digits = phone[1:]
        return all(char.isdigit() for char in digits)

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
        if not Phone.validate_phone(phone):
            raise ValueError("Invalid phone number format")
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return

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

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                if today <= birthday_date < next_week:
                    upcoming_birthdays.append(record.name.value)
        return upcoming_birthdays

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

book = AddressBook()

john_record = Record("John")
john_record.add_phone("+1234567890")
john_record.add_phone("+5555555555")
john_record.add_birthday("23.01.1985")

book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("+9876543210")
jane_record.add_birthday("27.01.1990")
book.add_record(jane_record)

print("All records in the address book:")
print(book)

john = book.find_record("John")
if john:
    john.edit_phone("+1234567890", "+1112223333")
    print("Updated John's record:")
    print(john)

if john:
    found_phone = john.find_phone("+5555555555")
    print(f"{john.name}: {found_phone}")

book.delete_record("Jane")
print("Address book after deleting Jane's record:")
print(book)

upcoming_birthday_names = book.get_upcoming_birthdays()
if upcoming_birthday_names:
    print("Users to congratulate next week:")
    print(", ".join(upcoming_birthday_names))
else:
    print("No upcoming birthdays next week")