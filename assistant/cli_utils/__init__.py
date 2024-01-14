from copy import deepcopy
from .utils import (
    register,
    listener,
    listener_command_param,
    get_success_message,
    get_warning_message,
    get_error_message,
    HANDLERS_SECTIONS,
    COMMAND_FOR_BREAK,
)
from .custom_prompt import CustomPrompt
from .custom_completion import CustomCompleter

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


@register("help", "system")
def command_help():
    return show_register_command()


__all__ = [
    "register",
    "listener",
    "listener_command_param",
    "get_success_message",
    "get_error_message",
    "get_warning_message",
    "show_register_command",
    "print_records",
    "CustomPrompt", 
    "CustomCompleter"
]
