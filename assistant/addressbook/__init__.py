from functools import wraps

from assistant.cli_utils import (
    register,
    get_success_message,
    get_warning_message,
    listener_command_param as listener_field,
    print_records,
)

from .addressbook import AddressBook
from .record import Record


def initialize():
    book = AddressBook()

    section = "contacts"

    def save_data(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            book.save_data()
            return result

        return wrapper

    @register("add-contact", section=section)
    @save_data
    def add(name: str) -> str:
        """
        Add contact with name address email birthday and phone
        """
        record = book.find(name)
        if record is None:
            record = Record(name)

        # key : "field name" , value : tuple(handler, required (True | False)) | handler
        fields_contact = {
            f"add-contact `{name}` address": record.add_address,
            f"add-contact `{name}` email": (record.add_email, True),
            f"add-contact `{name}` birthday": record.add_birthday,
        }

        for fields, handler in fields_contact.items():
            required = False
            if isinstance(handler, tuple):
                handler, required = handler
            while True:
                result_input = listener_field(fields, required)
                if len(result_input) == 0 and not required:
                    break

                try:
                    handler(result_input)
                    break
                except Exception as e:
                    print(get_warning_message(handler.__name__, e))

        # if not record.find_phone(phone_number) is None:
        #     raise ValueError(f"Phone number `{phone_number}` in contact `{name}` exist")

        # record.add_phone(phone_number)

        book.add(record)

        return get_success_message(f"Contact `{name}` added")

    @register("edit-contact", section=section, data_for_prompt=book)
    @save_data
    def edit(name: str) -> str:
        record = book.find(name)

        if record is None:
            raise ValueError(f"Contact with name `{name}` not exist")

        return get_success_message(f"Contact `{name}` edit")

    @register("edit-contact-birthday", section=section)
    @save_data
    def edit_birthday(name: str, date: str = None) -> str:
        record = book.find(name)

        if record is None:
            raise ValueError(f"Contact with name `{name}` not exist")

        if date is None:
            record.remove_birthday()
        else:
            record.edit_birthday(date)

        return get_success_message(f"Contact `{name}` birthday edit")

    @register("search-contact", section=section)
    def search(string_search: str):
        """
        Search name or phone in book
        """
        result_list = book.search(string_search)
        if len(result_list) == 0:
            raise ValueError("Nothing found")

        tab_result = [f"|{'NAME':^10}|"]
        tab_result.extend(list(f"|{str(name):^10}|" for name in result_list))

        return get_success_message("\n".join(tab_result))

    @register("show-contacts", section=section)
    def show_record():
        """
        Show all record
        """
        # list_record = list(get_success_message(f"{book[record]}") for record in book)
        return print_records(list(book.data.values()))

    @register("del-contact", section=section, data_for_prompt=book)
    @save_data
    def delete(name: str) -> str:
        """
        Remove contact by name
        """
        record = book.find(name)

        if record is None:
            raise ValueError(f"Contact with name `{name}` not exist")

        book.delete(name)

        return get_success_message(f"Contact witn `{name}` deleted")
