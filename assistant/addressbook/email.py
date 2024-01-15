from fields import Field
import re

class Email(Field):
    def __init__(self, email: str) -> None:
        super().__init__(self.__is_valid_email(email))

    @property
    def email(self):
        return self.value

    @email.setter
    def email(self, email: str):
        self.value = self.__is_valid_email(email)

    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$')

    def __is_valid_email(self, email):
        if isinstance(email, str):
            match_object = self.email_pattern.match(email)
            if match_object is not None:
                return match_object.group()
            else:
                print('Invalid email')
        else:
            print('Invalid email')

