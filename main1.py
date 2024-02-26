from collections import UserDict
from datetime import datetime, timedelta

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
    def __init__(self, contacts_file_path):
        super().__init__()
        self.contacts_file_path = contacts_file_path
        self.load_birthdays_from_file()

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
                birthday_date = birthday_date.replace(year=datetime.now().year)
                difference_days = (birthday_date - today).days
                if difference_days <= 7 and difference_days >= 0:
                    if birthday_date.weekday() >= 5:
                        days_until_monday = 7 - birthday_date.weekday()
                        birthday_date += timedelta(days=days_until_monday)
                    upcoming_birthdays.append({"name": record.name.value, "Congratulatinons_day": birthday_date.strftime("%Y.%m.%d")})
        return upcoming_birthdays

    def load_birthdays_from_file(self):
        try:
            with open(self.contacts_file_path, 'r') as file:
                for line in file:
                    name, *data = line.strip().split(',')
                    if len(data) == 1:
                        # Если дата рождения отсутствует в файле, создаем контакт без нее
                        record = Record(name)
                    elif len(data) == 2:
                        # Если дата рождения присутствует в файле, добавляем ее к контакту
                        record = Record(name)
                        record.add_birthday(data[1])
                    else:
                        # Неправильный формат строки, игнорируем ее
                        continue
                    self.add_record(record)
        except FileNotFoundError:
            pass


    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())