from functools import wraps

# from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import PromptSession


HANDLERS = {}
HANDLERS_SECTIONS = {}
COMMAND_PROMPT = ">>> "
COMMAND_USE_SPACER = ("show all", "good bye")
COMMAND_FOR_BREAK = ("good bye", "close", "exit")
DATA_FOR_COMMAND = {}
# COMMAND_HELP = ("help",)

# color for string
ERROR = "\033[91m"
SUCCESS = "\033[92m"
WARNING = "\033[33m"
RESET = "\033[0m"


def get_warning_message(func_name: str, message_warning: str) -> str:
    return f"{WARNING}!!! {func_name} command : {message_warning}{RESET}"


def get_success_message(message_success: str) -> str:
    return f"{SUCCESS}{message_success}{RESET}"


def get_error_message(message_error: str) -> str:
    return f"{ERROR}{message_error}{RESET}"


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
        list_command = command.split()

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


def listener_command_param(add_prompt: str, required: bool) -> tuple:
    while True:
        param = input(f"{COMMAND_PROMPT}{add_prompt} : ")

        result_input = param.strip()

        if not (required and len(result_input) == 0):
            break

    return result_input


def listener() -> None:
    session = PromptSession()

    dict_commands = dict.fromkeys(HANDLERS)
    for k, v in DATA_FOR_COMMAND.items():
        dict_commands[k] = dict.fromkeys(v)
    dict_commands.update(dict.fromkeys(COMMAND_FOR_BREAK).items())

    completer = NestedCompleter.from_nested_dict(dict_commands)

    while True:
        # command_user = input(COMMAND_PROMPT)
        command_user = session.prompt(
            COMMAND_PROMPT, completer=completer, auto_suggest=AutoSuggestFromHistory()
        )

        if len(command_user) == 0:
            continue

        command, *args = command_parser(command_user)

        if command in COMMAND_FOR_BREAK:
            print(f"{SUCCESS}Good bye!{RESET}")
            break

        if HANDLERS.get(command):
            if all(args):
                print(HANDLERS[command](*args))
            else:
                print(HANDLERS[command]())
        else:
            print(get_error_message(f"Unknown command : {command}"))
