from functools import partial

from copy import deepcopy
from .utils import (
    register,
    HANDLERS_SECTIONS,
    COMMAND_FOR_BREAK,
    command_parser,
    HANDLERS,
    dict_commands,
    update_data_for_command
)
from .message import (
    get_success_message,
    get_warning_message,
    get_error_message,
)
from .custom_prompt import CustomPrompt, break_prompt
from .custom_completion import CustomCompleter , get_nested_completer

from .printing import print_records


def add_system_command():
    new_commands_dict = deepcopy(HANDLERS_SECTIONS)  # do copy

    new_commands_dict.setdefault("system", [])
    new_commands_dict["system"] += list(COMMAND_FOR_BREAK)

    return new_commands_dict


def show_register_command() -> str:
    all_commmands = add_system_command()

    commands = list(
        f"{section.upper()} : {', '.join(values)}"
        for section, values in all_commmands.items()
    )
    format_commands = "\n\t ".join(commands)
    return get_success_message(f"All command : \n\t {format_commands}")


def listener():

    completer = get_nested_completer(dict_commands())
    update_data_for_command(completer)

    main_prompt = CustomPrompt(
        command_prompt="",
        completer=completer,
        command_for_break=COMMAND_FOR_BREAK,
        command_parser=command_parser,
        command_handler=HANDLERS,
        post_handlers=[partial(update_data_for_command, completer)]
    )

    main_prompt()


@register("help", "system")
def command_help():
    return show_register_command()


__all__ = [
    "register",
    "listener",
    "get_success_message",
    "get_error_message",
    "get_warning_message",
    "show_register_command",
    "print_records",
    "CustomPrompt",
    "CustomCompleter",
    "break_prompt"
]
