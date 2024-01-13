from collections import UserDict
import pickle

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
        with open("db_contact.bin", "wb") as file:
            pickle.dump(self, file)

    def load_data(self):
        try:
            with open("db_contact.bin", "rb") as file:
                unpacked = pickle.load(file)
            # self.limit = unpacked.limit
            self.data = unpacked.data
        except FileNotFoundError:
            pass

    def __iter__(self):
        return iter(self.data)

    # def __next__(self):
    #    pass
