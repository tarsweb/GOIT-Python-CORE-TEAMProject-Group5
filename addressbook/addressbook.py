from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name: str):
        super().__init__(self.__is_valid_name(name))

    @property
    def name(self):
        return self.value

    @name.setter
    def name(self, name):
        self.value = self.__is_valid_name(name)

    @staticmethod
    def __is_valid_name(name: str):
        if not name:
            raise ValueError("Name is required")
        return name


class Record:
    def __init__(self, name: str):
        self.name = Name(name)

    def __str__(self) -> str:
        return f"{self.name}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record) -> None:
        self.data[record.name.name] = record

    def __iter__(self):
        return iter(self.data)

    #def __next__(self):
    #    pass
