from collections import UserList
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
        pass

    def load_data(self):
        pass

    def __iter__(self):
        return iter(self.data)

    def __next__(self):
        pass
