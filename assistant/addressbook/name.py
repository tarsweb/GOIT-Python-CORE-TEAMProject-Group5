from .fields import Field


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
