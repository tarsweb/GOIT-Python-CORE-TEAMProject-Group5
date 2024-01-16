from .fields import Field


class Address(Field):
    def __init__(self, address: str)-> None:
        super().__init__(address)

    @property
    def address(self):
        return self.value

    @address.setter
    def address(self, value):
        self.value = value

    def __str__(self):
        return "-" if self.address is None else str(self.address)
