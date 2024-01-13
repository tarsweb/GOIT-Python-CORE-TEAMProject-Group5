from .utils import (
    register,
    listener,
    get_success_message,
    get_warning_message,
    get_error_message,
    HANDLERS_SECTIONS,
    COMMAND_FOR_BREAK,
)


def show_register_command() -> str:

    _handlers_section = dict(HANDLERS_SECTIONS) # do copy

    _handlers_section.setdefault("system", [])
    _handlers_section["system"].extend(list(COMMAND_FOR_BREAK))

    commands = list(
        f"{section.upper()} : {', '.join(values)}"
        for section, values in _handlers_section.items()
    )
    format_commands = "\n\t ".join(commands)
    return get_success_message(
        f"All command : \n\t {format_commands}"
    )


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
]
