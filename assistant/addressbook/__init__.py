from functools import wraps
from collections import namedtuple
from functools import partial


from cli_utils import (
    register,
    get_success_message,
    get_warning_message,
    print_records,
    CustomPrompt,
    CustomCompleter,
    break_prompt,
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

        custom_prompt = f"add-contact `{name}`"

        def apply_result(handler, post_handler=None):
            def res(*agrs):
                try:
                    handler(*agrs)
                    if callable(post_handler):
                        return post_handler()
                except Exception as e:
                    print(get_warning_message(handler.__name__, e))

            return res

        def command_parser(required: bool, value: str) -> tuple:
            if required is None:
                required = False
            if len(value) == 0 and not required:
                return ("break",)

            return "add", value

        def global_post_handler(record_field: str) -> None | str:
            try:
                if str(getattr(record, record_field)):
                    return break_prompt()
            except Exception:
                return

        def phone_post_handler():
            try:
                if len(record.phones) > 0:
                    answer = False

                    def answer_command_parser(value):
                        nonlocal answer
                        if value.lower() in ("n", "no") or len(value) == 0:
                            answer = True
                            return ("no",)

                    questions_dict = {
                        "yes": {"display_meta": "add more phone"},
                        "no": {"display_meta": " no enough "},
                    }
                    add_more_completer = CustomCompleter(questions_dict)
                    prompt_add_more = CustomPrompt(
                        command_prompt=f"{custom_prompt} {'phone'.capitalize()} Add more ? ",
                        completer=add_more_completer,
                        command_for_break=(),
                        command_parser=answer_command_parser,
                        command_handler={"yes": None, "no": break_prompt},
                        placeholder="yes/no",
                        ignore_empty_command=False,
                    )
                    prompt_add_more()

                    if answer:
                        return break_prompt()

            except Exception:
                return

        Action_params = namedtuple(
            "action_param",
            ["handler", "post_handler", "required", "multi", "placeholder"],
            defaults=(None, None, False, False, ""),
        )
        # actions_prompt = CustomPrompt(custom_prompt, None, ("N",))
        actions_contact = {
            "address": Action_params(
                record.add_address, partial(global_post_handler, "address")
            ),
            "email": Action_params(
                record.add_email, partial(global_post_handler, "email"), True
            ),
            "birthday": Action_params(
                record.add_birthday, partial(global_post_handler, "birthday")
            ),
            "phone": Action_params(
                record.add_phone, phone_post_handler, False, True, "--phone number--"
            ),
        }

        for action, param_actions in actions_contact.items():
            required = False
            multi = False
            placeholder = ""
            post_handler = None
            if isinstance(param_actions, (tuple, namedtuple)):
                handler, post_handler, required, multi, placeholder = param_actions
            else:
                handler = param_actions

            actions_prompt = CustomPrompt(
                command_prompt=f"{custom_prompt} {action.capitalize()} ",
                completer=None,
                command_for_break=("n", "no", "NO"),
                command_parser=partial(command_parser, required),
                command_handler={
                    "add": apply_result(handler, post_handler),
                    "break": break_prompt,
                },
                placeholder=placeholder if placeholder else action,
                required=required,
                ignore_empty_command=False,
            )
            # actions_prompt.command_prompt = f"{custom_prompt}{action}"
            # actions_prompt.command_parser = command_parser
            # actions_prompt.command_handler =  {"add": aply_res(handler), "close": print}
            # actions_prompt.required = required

            actions_prompt()

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
