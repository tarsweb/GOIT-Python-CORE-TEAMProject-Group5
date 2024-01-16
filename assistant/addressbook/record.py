from datetime import date

from .name import Name
from .email import Email
from .address import Address
from .birthday import Birthday
from .phone import Phone


class Record:
    def __init__(
        self, name: str, address: str = None, email: str = None, birthday: str = None
    ):
        self.name = Name(name)
        self.address = Address(address)
        self.email = Email(email)
        self.birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, phone_number: str) -> None:
        phone = self.find_phone(phone_number)

        if phone:
            raise ValueError(f"Phone number {phone_number} exist")

        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        self.phones = list(
            filter(lambda phone: phone.value != phone_number, self.phones)
        )

    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> None:
        phone_record = self.find_phone(old_phone_number)
        if phone_record is None:
            raise ValueError("Phone {old_phone_number} not found")
        phone_record.phone = new_phone_number

    def find_phone(self, phone_number) -> Phone | None:
        phones_find = tuple(
            filter(lambda phone: phone.phone == phone_number, self.phones)
        )
        if len(phones_find) > 0:
            return phones_find[0]

    def add_birthday(self, day_birthday: str) -> None:
        self.birthday.birthday_date = day_birthday

    def remove_birthday(self) -> None:
        self.birthday.birthday_date = None

    def edit_birthday(self, day_birthday: str) -> None:
        self.birthday.birthday_date = day_birthday

    def days_to_birthday(self) -> int | None:
        if self.birthday.birthday_date is not None:
            current_day = date.today()
            offset_year = 0
            month_birthday, day_birthday = (
                self.birthday.birthday_date.month,
                self.birthday.birthday_date.day,
            )
            if (current_day.month > month_birthday) or (
                current_day.month == month_birthday and current_day.day > day_birthday
            ):
                offset_year = 1

            current_birthday = self.birthday.birthday_date.replace(
                year=current_day.year + offset_year
            )

            return (current_birthday - current_day).days

    def add_address(self, address: str) -> None:
        self.address.address = address

    def remove_address(self) -> None:
        self.address.address = None

    def add_email(self, email: str) -> None:
        self.email.email = email

    def remove_email(self) -> None:
        self.email.email = None

    def __str__(self) -> str:
        return (
            f"Contact Name: `{self.name}` Address: `{self.address}` E-mail: `{self.email}`"
            f"Birthday: `{self.birthday}` Phones: `{'; '.join(p.value for p in self.phones)}`"
        )
