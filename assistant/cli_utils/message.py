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