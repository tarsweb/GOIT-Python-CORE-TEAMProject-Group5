from functools import wraps, partial
from collections import namedtuple
from collections.abc import Iterable
from copy import deepcopy

from cli_utils import (
    register,
    get_success_message,
    get_warning_message,
    print_records,
    CustomPrompt,
    CustomCompleter,
    get_nested_completer,
    break_prompt,
    Action_params,
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
                        command_for_break=tuple(),
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
                command_for_break=("n", "no"),
                command_parser=partial(command_parser, required),
                command_handler={
                    "add": apply_result(handler, post_handler),
                    "break": break_prompt,
                },
                placeholder=placeholder if placeholder else action,
                required=required,
                ignore_empty_command=False,
            )
            actions_prompt()

        book.add(record)

        return get_success_message(f"Contact `{name}` added")

    @register("edit-contact", section=section, data_for_prompt=book)
    # @save_data
    def edit(name: str) -> str:
        record = book.find(name)

        if record is None:
            raise ValueError(f"Contact with name `{name}` not exist")

        temp_record = deepcopy(record)

        custom_prompt = f"edit-contact `{name}`"
        field_names = record.__dict__.keys()

        field_dict = list(
            field
            for field in field_names
            if isinstance(getattr(record, field), Iterable)
        )

        exc_dict = {}
        _ = [exc_dict.update({f"{i}": []}) for i in field_names]

        def apply_result(handler, post_handler=None):
            def res(*agrs):
                try:
                    handler(*agrs)
                    if callable(post_handler):
                        return post_handler()
                except Exception as e:
                    print(get_warning_message(handler.__name__, e))

            return res

        req = ("name", "email")

        def command_parser(required: bool, value: str) -> tuple:
            if required is None:
                required = False
            if len(value) == 0 and not required:
                # if value.startswith("save"):
                #     return save_changes()
                return ("break",)

            value.strip()
            if value.startswith(req):
                command = value.split(maxsplit=1)
            else:
                command = value.split(maxsplit=2)

            if len(command) == 1:
                return (*command, None)
            return (
                "-".join(map(lambda n: n.lower(), command[:2])),
                tuple(map(lambda n: n.lower(), command[:2])), command[2:]
            )

        def save_changes():
            return break_prompt()

        def cancel_changes():
            nonlocal exc_dict
            exc_dict = {}
            return break_prompt()

        handelrs = {
            "name-edit": None,
            "name-remove": None,
            "address-edit": temp_record.add_address,
            "address-remove": temp_record.remove_address,
            "email-edit": temp_record.add_email,
            "email-remove": temp_record.remove_email,
            "birthday-edit": temp_record.add_birthday,
            "birthday-remove": temp_record.remove_birthday,
            "phones-add": temp_record.add_phone,
            "phones-edit": temp_record.edit_phone,
            "phones-remove": temp_record.remove_phone,
        }

        def handler(*args):
            nonlocal exc_dict
            print("handler", *args)
            _command, data = args
            command_execute = handelrs.get("-".join(_command))
            try:
                if command_execute.__name__ == "edit_phone":
                    command_execute(" ".join(data).split(maxsplit=1))
                else:
                    if len(data) == 0:
                        command_execute()
                    else:
                        command_execute(" ".join(data))
                field, _ = _command
                if field in exc_dict:
                    exc_dict[field] += [*exc_dict[field], {command_execute.__name__: data}]
            except Exception as e:
                print(get_warning_message(command_execute.__name__, e))

            print(_command, data)

        completer_command = get_nested_completer(dict.fromkeys(("edit", "remove")))

        completers_iterable = {}
        for iterable_f in field_dict:
            atr_array = [str(el) for el in getattr(record, iterable_f)]
            completers_for_iter = get_nested_completer(dict.fromkeys(atr_array))
            completers_iterable[iterable_f.capitalize()] = completers_for_iter

        dict_command = dict.fromkeys(list(f.capitalize() for f in req))
        dict_command.update(
            dict.fromkeys(
                list(f.capitalize() for f in field_names if f not in req),
                completer_command,
            )
        )
        dict_command.update(dict.fromkeys(("save", "cancel")))

        completer = get_nested_completer(dict_command)

        for k, v in completers_iterable.items():
            completer_command = get_nested_completer(
                dict.fromkeys(("add", "edit", "remove"))
            )
            for command in completer_command.options:
                if not command == "add":
                    completer_command.options[command] = v

            completer.options[k] = completer_command

        command_handler = {
            "save": save_changes, #apply_result(handler,None),
            "cancel": cancel_changes,
        }
        _ = [
            command_handler.update({f"{i}-edit": handler, f"{i}-remove": handler})
            for i in field_names
        ]
        _ = [command_handler.update({f"{i}-add": handler}) for i in field_dict]

        actions_prompt = CustomPrompt(
            command_prompt=f"{custom_prompt} ",
            completer=completer,
            command_for_break=("n", "no"),
            command_parser=partial(command_parser, False),
            command_handler=command_handler,
            placeholder="select field / command",
            ignore_empty_command=False,
        )
        actions_prompt()

        print(*exc_dict)

        for k,v in exc_dict.items():
            for action in v:
                for command , data in action.items():
                    eval(f"record.{command}('{' '.join(data)}')")

        return get_success_message(f"Contact `{name}` edit")

    # @register("edit-contact-birthday", section=section)
    # @save_data
    # def edit_birthday(name: str, date: str = None) -> str:
    #     record = book.find(name)

    #     if record is None:
    #         raise ValueError(f"Contact with name `{name}` not exist")

    #     if date is None:
    #         record.remove_birthday()
    #     else:
    #         record.edit_birthday(date)

    #     return get_success_message(f"Contact `{name}` birthday edit")

    @register("contact-birthday", section=section)
    def contact_birthday_from(count_days: str):
        try:
            count_days = int(count_days)
        except ValueError as e:
            raise ValueError("Param may be integer") from e

        result_list = list(
            record
            for record in book.values()
            if record.days_to_birthday() == count_days
        )
        if len(result_list) == 0:
            raise ValueError(f"Nothing contact birthday in {count_days} days")

        return print_records(result_list)

    @register("search-contact", section=section)
    def search(string_search: str):
        """
        Search name or phone in book
        """

        if len(book.data) == 0:
            raise ValueError("No contact")

        result_list = book.search(string_search.lower())
        if len(result_list) == 0:
            raise ValueError("Nothing found")

        return print_records(result_list)

    @register("show-contacts", section=section)
    def show_record():
        """
        Show all record
        """
        if len(book.data) == 0:
            raise ValueError("No contact")

        return print_records(list(book.data.values()))

    @register("remove-contact", section=section, data_for_prompt=book)
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
