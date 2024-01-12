from collections import UserDict
from .record import Record


class AddressBook(UserDict):
    # def __init__(self):
    #     super().__init__()

    def add(self, record: Record) -> None:
        self.data[record.name.name] = record

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def find(self, name: str) -> Record | None:
        if name in self.data:
            return self.data[name]

    def search(self, search_string: str) -> list:
        pass

    def save_data(self):
        pass

    def load_data(self):
        pass

    def __iter__(self):
        return iter(self.data)

    # def __next__(self):
    #    pass
