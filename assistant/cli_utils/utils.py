from functools import wraps

# from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from .message import get_warning_message, get_success_message, get_error_message

HANDLERS = {}
HANDLERS_SECTIONS = {}
COMMAND_PROMPT = ">>> "
COMMAND_USE_SPACER = ("show all", "good bye")
COMMAND_FOR_BREAK = ("good bye", "close", "exit")
DATA_FOR_COMMAND = {}


def input_error(func):
    def string_error_message(message: str) -> str:
        return message.replace(str(func.__qualname__) + "()", "")

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as te:
            return get_warning_message(func.__name__, string_error_message(str(te)))
        except KeyError as ke:
            return get_warning_message(func.__name__, string_error_message(str(ke)))
        except ValueError as ve:
            return get_warning_message(func.__name__, string_error_message(str(ve)))
        except IndexError as ie:
            return get_warning_message(func.__name__, string_error_message(str(ie)))

    return wrapper


def command_parser(command_string: str) -> tuple:
    command = command_string.strip()
    if command.lower() in COMMAND_USE_SPACER:
        list_command = [command]
    else:
        list_command = command.split(maxsplit=1)

    if len(list_command) == 1:
        return list_command[0].lower(), None

    return list_command[0].lower(), *list_command[1:]


def register(commmand_name: str, section: str = None, data_for_prompt: dict = None):
    def register_wrapper(func):
        @input_error
        @wraps(func)
        def wrapper(*agrs, **kwargs):
            result = func(*agrs, **kwargs)
            return result

        HANDLERS[commmand_name] = wrapper

        key_for_section = "users" if not section else section
        HANDLERS_SECTIONS.setdefault(key_for_section, [])
        HANDLERS_SECTIONS[key_for_section].append(commmand_name)

        if not data_for_prompt is None:
            DATA_FOR_COMMAND[commmand_name] = data_for_prompt

        return wrapper

    return register_wrapper


def listener_command_param(add_prompt: str, required: bool) -> str:
    while True:
        param = input(f"{COMMAND_PROMPT}{add_prompt} : ")

        result_input = param.strip()

        if not (required and len(result_input) == 0):
            break

    return result_input


def update_data_for_command(completer: NestedCompleter) -> None:
    for k, v in DATA_FOR_COMMAND.items():
        completer.options[k] = NestedCompleter.from_nested_dict(dict.fromkeys(v))


def dict_commands() -> dict:
    commands = dict.fromkeys(HANDLERS)
    commands.update(dict.fromkeys(COMMAND_FOR_BREAK).items())

    return commands


# def listener() -> None:
#     session = PromptSession(
#         COMMAND_PROMPT, 
#         complete_while_typing=True, 
#         mouse_support=True
#     )

#     completer = NestedCompleter.from_nested_dict(dict_commands())
#     update_data_for_command(completer)

#     while True:
#         # command_user = input(COMMAND_PROMPT)
#         command_user = session.prompt(
#             completer=completer,
#             auto_suggest=AutoSuggestFromHistory(),
#         )

#         if len(command_user) == 0:
#             continue

#         command, *args = command_parser(command_user)

#         if command in COMMAND_FOR_BREAK:
#             print(get_success_message("Good bye!"))
#             break

#         if HANDLERS.get(command):
#             if all(args):
#                 print(HANDLERS[command](*args))
#             else:
#                 print(HANDLERS[command]())
#         else:
#             print(get_error_message(f"Unknown command : {command}"))

#         update_data_for_command(completer)
