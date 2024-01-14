from typing import Any
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from .utils import COMMAND_PROMPT as MAIN_PROMPT, get_error_message

# color for string
ERROR = "\033[91m"
SUCCESS = "\033[92m"
WARNING = "\033[33m"
RESET = "\033[0m"

class CustomPrompt:
    def __init__(
        self,
        command_prompt: str,
        completer: Completer,
        command_for_break: str | tuple,
        command_parser,
        command_handler,
        placeholder: str = "",
        single: bool = True,
        required: bool = False
    ) -> None:
        self.command_prompt = command_prompt
        self.command_for_break = command_for_break
        self.command_parser = command_parser
        self.completer = completer
        self.command_handler = command_handler
        self.placeholder = placeholder
        self.__single = single
        self.__required = required

    @property
    def required(self):
        return " * " if self.__required else ""

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        session = PromptSession(
            f"{MAIN_PROMPT}{self.command_prompt}{self.required}",
            complete_while_typing=True,
            mouse_support=True,
            placeholder=self.placeholder,
        )

        while True:
            command = session.prompt(
                completer=self.completer,
                auto_suggest=AutoSuggestFromHistory(),
            )

            if command in self.command_for_break:
                print("break")
                break

            command, *args = self.command_parser(command)  # maybe **kwargs not now

            if self.command_handler.get(command):
                if all(args):
                    print(self.command_handler[command](*args))
                else:
                    print(self.command_handler[command]())
            else:
                get_error_message(f"Unknown command : {command}")
