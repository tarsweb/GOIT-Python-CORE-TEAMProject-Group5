from collections import UserList
from contextlib import suppress
import json
from .record import Record


class Note(UserList):
    def add(self, record: Record) -> None:
        self.data.append(record)

    def delete(self, index: int) -> None:
        pass

    def find(self, index: int) -> Record | None:
        if len(self.data) > index:
            return self.data[index]

    def search(self, search_string: str) -> list:
        pass

    def save_data(self):
        database = {}
        with suppress(FileNotFoundError):
            with open(file="db.json", mode="r", encoding="utf8") as file:
                text = file.read()
                database = json.loads(text)
        for record_data in self.data:
            with suppress(AttributeError):
                record = {
                    "text": record_data["text"],
                    "tags": record_data["tags"],
                }
                database["notes"].append(record)
        with open(file="db.json", mode="w", encoding="utf8") as file:
            text = json.dumps(database)
            file.write(text)


    def load_data(self):
        with suppress(FileNotFoundError):
            with open(file="db.json", mode="r", encoding="utf8") as file:
                text = file.read()
                data = json.loads(text)
                if data:
                    for name, record_data in data["book"].items():
                        record = Record(name)
                        record.add_address(record_data["address"])
                        record.add_email(record_data["email"])
                        record.add_birthday(record_data["birthday"])
                        for phone in record_data["phones"]:
                            record.add_phone(phone)
                        self.data[name] = record

    def __iter__(self):
        return iter(self.data)

    def __next__(self):
        pass
