from collections import UserList
from contextlib import suppress
import json
from .record import Record


class Note(UserList):
    def __init__(self) -> None:
        super().__init__()
        self.load_data()

    def add(self, record: Record) -> None:
        self.data.append(record)

    def delete(self, record: Record) -> None:
        self.data.remove(record)

    def find(self, index: int) -> Record | None:
        if len(self.data) > index:
            return self.data[index]

    def find_notes_by_tags(self, tag: str) -> list:
        return list(record for record in self.data if tag in record.tags)

    def search(self, search_string: str) -> list:
        result = []
        for record in self.data:
            if record.text.lower().find(search_string) != -1:
                result.append(record)
                continue
            for tag in record.tags:
                if tag.lower().find(search_string) != -1:
                    result.append(record)
                    break
        return result

    def save_data(self) -> None:
        database = {}
        with suppress(FileNotFoundError):
            with open(file="db.json", mode="r", encoding="utf8") as file:
                text = file.read()
                database = json.loads(text)
                records = [
                    {"text": record.text, "tags": record.tags} for record in self.data
                ]
                database["notes"] = records
        with open(file="db.json", mode="w", encoding="utf8") as file:
            json.dump(database, file, indent=4, ensure_ascii=False)

    def load_data(self) -> None:
        with suppress(FileNotFoundError):
            with open(file="db.json", mode="r", encoding="utf8") as file:
                text = file.read()
                data = json.loads(text)
                if data:
                    for record_data in data["notes"]:
                        record = Record(record_data["text"])
                        for tag in record_data["tags"]:
                            record.add_tag(tag)
                        self.data.append(record)

    def __iter__(self):
        return iter(self.data)

    def __next__(self):
        pass
