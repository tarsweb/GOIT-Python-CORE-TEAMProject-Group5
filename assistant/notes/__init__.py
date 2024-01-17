from functools import wraps, partial
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
)

from .notes import Note
from .record import Record


def initialize():
    notes = Note()

    section = "notes"

    def save_data(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            notes.save_data()
            return result

        return wrapper

    def handler_data_prompt(data) -> dict:
        return {
            data.index(i)
            + 1: {"display": i.text[:20], "display_meta": ", ".join(i.tags)}
            for i in data
        }

    def handler_data_prompt_tag(data) -> dict:
        result = []
        _ = set(result.extend(i.tags) for i in data)
        return dict.fromkeys(
            result,
        )

    @register("add-note", section=section)
    @save_data
    def add(text: str) -> None:
        """
        Add notes
        """

        record = Record(text=text)

        custom_prompt = f"add-note `{text}`"
        actions = "tag"

        def apply_result(handler, post_handler=None):
            def res(*agrs):
                try:
                    handler(*agrs)
                    if callable(post_handler):
                        return post_handler()
                except Exception as e:
                    print(get_warning_message(handler.__name__, e))

            return res

        def command_parser(value: str) -> tuple:
            if len(value) == 0:
                return ("break",)

            return "add", value

        def tag_post_handler():
            try:
                if len(record.tags) > 0:
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
                        command_prompt=f"{custom_prompt} {actions.capitalize()} Add more ? ",
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

        tag_prompt = CustomPrompt(
            command_prompt=f"{custom_prompt} {actions.capitalize()} ",
            completer=None,
            command_for_break=("n", "no"),
            command_parser=command_parser,
            command_handler={
                "add": apply_result(record.add_tag, tag_post_handler),
                "break": break_prompt,
            },
            placeholder="type tag",
            ignore_empty_command=False,
        )

        tag_prompt()

        notes.add(record)

        return get_success_message(f"Note `{text}` added")

    @register(
        "edit-note",
        section=section,
        data_for_prompt=notes,
        handler_data_prompt=handler_data_prompt,
    )
    @save_data
    def edit(index: str) -> None:
        """
        Edit note
        """

        try:
            index = int(index) - 1
        except ValueError as e:
            raise ValueError("Index for note may be integer") from e

        record = notes.find(index)

        if record is None:
            raise ValueError(f"Note with index `{index}` not exist")

        temp_record = deepcopy(record)

        record_edit = False
        custom_prompt = f"edit-note `{record.text}`"
        field_names = temp_record.__dict__.keys()

        field_dict = list(
            field
            for field in field_names
            if isinstance(getattr(record, field), Iterable)
            and not isinstance(getattr(record, field), str)
        )

        required_field = ("text",)

        def command_parser(required: bool, value: str) -> tuple:
            if required is None:
                required = False
            if len(value) == 0 and not required:
                return ("break",)

            value.strip()
            if value.startswith(
                tuple(req_command.capitalize() for req_command in required_field)
            ):
                value = "".join(
                    tuple(
                        value.replace(req_c.capitalize(), f"{req_c.capitalize()} edit")
                        for req_c in required_field
                        if value.startswith(req_c.capitalize())
                    )
                )

            command = value.split(maxsplit=2)

            if len(command) == 1:
                return (*command, None)
            return (
                "-".join(map(lambda n: n.lower(), command[:2])),
                tuple(map(lambda n: n.lower(), command[:2])),
                command[2:],
            )

        def save_changes():
            return break_prompt()

        def cancel_changes():
            nonlocal record_edit
            record_edit = False
            return break_prompt()

        handelrs_record = {
            "text-edit": temp_record.edit_text,
            "text-remove": temp_record.remove_text,
            "tags-add": temp_record.add_tag,
            "tags-edit": temp_record.edit_tag,
            "tags-remove": temp_record.remove_tag,
        }

        def command_record_handler(*args):
            nonlocal record_edit
            _command, data = args
            command_execute = handelrs_record.get("-".join(_command))
            try:
                if command_execute.__name__ == "edit_tag":
                    old_phone, new_phone = " ".join(data).split(maxsplit=1)
                    command_execute(old_phone, new_phone)
                else:
                    if all(args):
                        command_execute(" ".join(data))
                    else:
                        command_execute()
                record_edit = True
            except Exception as e:
                print(get_warning_message(command_execute.__name__, e))

        completer_command = get_nested_completer(dict.fromkeys(("edit", "remove")))

        completers_iterable = {}

        def upadate_data():
            nonlocal completers_iterable
            for iterable_f in field_dict:
                atr_array = [str(el) for el in getattr(temp_record, iterable_f)]
                completers_for_iter = get_nested_completer(dict.fromkeys(atr_array))
                completers_iterable[iterable_f.capitalize()] = completers_for_iter

        dict_command = dict.fromkeys(list(f.capitalize() for f in required_field))
        dict_command.update(
            dict.fromkeys(
                list(f.capitalize() for f in field_names if f not in required_field),
                completer_command,
            )
        )
        system_commands = ("save", "cancel")
        dict_command.update(dict.fromkeys(system_commands))
        completer = get_nested_completer(dict_command)
        upadate_data()

        def use_update_data():
            nonlocal completer
            for k, v in completers_iterable.items():
                completer_command = get_nested_completer(
                    dict.fromkeys(("add", "edit", "remove"))
                )
                for command in completer_command.options:
                    if not command == "add":
                        completer_command.options[command] = v

                completer.options[k] = completer_command

        use_update_data()

        prompt_command_handler = {
            "save": save_changes,  # apply_result(handler,None),
            "cancel": cancel_changes,
            "break": None,
        }
        _ = [
            prompt_command_handler.update(
                {
                    f"{i}-edit": command_record_handler,
                    f"{i}-remove": command_record_handler,
                }
            )
            for i in field_names
        ]
        _ = [
            prompt_command_handler.update({f"{i}-add": command_record_handler})
            for i in field_dict
        ]

        actions_prompt = CustomPrompt(
            command_prompt=f"{custom_prompt} ",
            completer=completer,
            command_for_break=(),
            command_parser=partial(command_parser, False),
            command_handler=prompt_command_handler,
            placeholder="select field / command",
            ignore_empty_command=False,
            post_handlers=[upadate_data, use_update_data],
        )

        actions_prompt()

        if record_edit:
            notes.data[index] = temp_record
            # only for view
            record = temp_record

        submessage = "" if record_edit else "cancel "
        return get_success_message(f"Note `{record.text}` {submessage}edited'")

    @register("search-note", section=section)
    def search(string_search: str):
        """
        Search text or tag in notes
        """
        if len(notes.data) == 0:
            raise ValueError("No notes")

        result_list = notes.search(string_search.lower())

        if len(result_list) == 0:
            raise ValueError("Nothing found")

        return print_records(result_list)

    @register(
        "search-note-tag",
        section=section,
        data_for_prompt=notes,
        handler_data_prompt=handler_data_prompt_tag,
    )
    def search_tag(string_search: str):
        """
        Search tag in tags
        """
        if len(notes.data) == 0:
            raise ValueError("No notes")

        result_list = notes.find_notes_by_tags(string_search.lower())

        if len(result_list) == 0:
            raise ValueError("Nothing found")

        return print_records(result_list)

    @register("show-notes", section=section)
    def show() -> str:
        """
        Show all notes
        """

        if len(notes.data) == 0:
            raise ValueError("No notes")

        return print_records(notes.data)

    @register(
        "remove-note",
        section=section,
        data_for_prompt=notes,
        handler_data_prompt=handler_data_prompt,
    )
    @save_data
    def delete(index: str) -> str:
        """
        Remove contact by name
        """
        try:
            index = int(index) - 1
        except ValueError as e:
            raise ValueError("Index for note may be integer") from e

        record = notes.find(index)

        if record is None:
            raise ValueError(f"Note with index `{index}` not exist")

        notes.delete(record)

        return get_success_message(f"Note with `{index}` deleted")
