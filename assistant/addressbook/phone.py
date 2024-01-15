from fields import Field
import re

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
        phone_number_pattern = re.compile(r'^\+\d{12}$')
        match_object = phone_number_pattern.match(phone_number)
        if match_object is not None:
            print(match_object.group())
            return match_object.group()
        else:
            print(f"Phone {phone_number} not valid")

