from datetime import date
from .fields import Field


class Birthday(Field):
    def __init__(self, birthday: str) -> None:
        super().__init__(self.__is_valid_birthday(birthday))

    @property
    def birthday_date(self):
        return self.value

    @birthday_date.setter
    def birthday_date(self, birthday: str):
        self.value = self.__is_valid_birthday(birthday)

    @staticmethod
    def __is_valid_birthday(birthday: str) -> date:
        if not birthday is None:
            try:
                date_list_of_birthday = [int(i) for i in birthday.split(".")]
                date_birthday = date(*date_list_of_birthday)
                return date_birthday
            except Exception:  # Exception on any types
                raise ValueError("birthday must have YYYY.MM.DD format!")

    def __str__(self):
        return "unknown" if self.birthday_date is None else str(self.birthday_date)
