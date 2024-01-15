from collections import UserDict
from contextlib import suppress
import json
from .record import Record


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.load_data()

    def add(self, record: Record) -> None:
        self.data[record.name.name] = record

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def find(self, name: str) -> Record | None:
        if name in self.data:
            return self.data[name]

    def search(self, search_string: str) -> list:
        result = []
        for record in self.data.values():
            if record.name.name.find(search_string) != -1:
                result.append(record.name)
                continue
            for phone_number in record.phones:
                if phone_number.phone.find(search_string) != -1:
                    result.append(record.name)
                break

        return result

    def save_data(self):
        database = {}
        with suppress(FileNotFoundError):
            with open(file="db.json", mode="r", encoding="utf8") as file:
                text = file.read()
                database = json.loads(text)
        for name, record_data in self.data.items():
            with suppress(AttributeError):
                record = {
                    "name": record_data.name.value,
                    "address": record_data.address.value or "",
                    "email": record_data.email.value,
                    "birthday": record_data.birthday.birthday_date.strftime("%Y.%m.%d")
                    if record_data.birthday.value
                    else "",
                    "phones": [record.value for record in record_data.phones],
                }
                database["book"].setdefault(name, record)
        with open(file="db.json", mode="w", encoding="utf8") as file:
            text = json.dumps(database)
            file.write(text)

    def load_data(self) -> None:
        with suppress(FileNotFoundError):
            with open(file="db.json", mode="r", encoding="utf8") as file:
                text = file.read()
                data = json.loads(text)
                if data:
                    for name, record_data in data["book"].items():
                        record = Record(name)
                        record.add_address(record_data["address"])
                        record.add_email(record_data["email"])
                        if len(record_data["birthday"]) > 0:
                            record.add_birthday(record_data["birthday"])
                        for phone in record_data["phones"]:
                            record.add_phone(phone)
                        self.data[name] = record

    def __iter__(self):
        return iter(self.data)

    # def __next__(self):
    #    pass
