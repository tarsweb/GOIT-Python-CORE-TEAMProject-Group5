from collections import UserDict
from .record import Record


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record) -> None:
        self.data[record.name.name] = record

    def __iter__(self):
        return iter(self.data)

    # def __next__(self):
    #    pass
