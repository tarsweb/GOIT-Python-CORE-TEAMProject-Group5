from .fields import Field


class Phone(Field):
    # реалізація класу
    def __init__(self, phone_number: str):
        super().__init__(self.__is_valid_phone_number(phone_number))

    @property
    def phone(self):
        return self.value

    @phone.setter
    def phone(self, phone_number):
        self.value = self.__is_valid_phone_number(phone_number)

    @staticmethod
    def __is_valid_phone_number(phone_number: str) -> str:
        if len(phone_number) == 10 and phone_number.isdigit():
            return phone_number
        raise ValueError(f"Phone {phone_number} not valid")
