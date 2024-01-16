from functools import wraps
from cli_utils.printing import print_records
from cli_utils import (
    register,
    get_success_message,
    get_warning_message,
    CustomCompleter,
    CustomPrompt,
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
        return dict.fromkeys(result, )

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

        return get_success_message(f"Note `{record}` edit")

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
