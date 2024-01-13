from .fields import Field
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

    @staticmethod
    def __is_valid_email(email: str) -> str | Exception:
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$")
        if isinstance(email, str):
            match_object = email_pattern.match(email)
            print(match_object)
            if match_object is not None:
                return match_object.group()
            else:
                raise ValueError("Invalid email")
        else:
            raise ValueError("Invalid email")

    def __str__(self):
        return "unknown" if self.email is None else str(self.email)


# from .fields import Field


# class Email(Field):
#     def __init__(self, email: str):
#         super().__init__(self.__is_valid_email(email))

#     @property
#     def email(self):
#         return self.value

#     @email.setter
#     def email(self, value):
#         self.value = self.__is_valid_email(value)

#     @staticmethod
#     def __is_valid_email(email: str):
#         # if not email:
#         #     raise ValueError("Email is required")
#         return email

#     def __str__(self):
#         return "unknown" if self.email is None else str(self.email)
