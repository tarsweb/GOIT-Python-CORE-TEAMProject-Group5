from typing import Any
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import to_formatted_text

from .utils import COMMAND_PROMPT as MAIN_PROMPT, get_error_message


class CustomPrompt:
    def __init__(
        self,
        command_prompt: str,
        completer: Completer | None,
        command_for_break: str | tuple,
        command_parser=None,
        command_handler=None,
        placeholder: str = "",
        # single: bool = True,
        required: bool = False,
        ignore_empty_command: bool = True,
        post_handlers=None,
    ) -> None:
        self.__command_prompt = command_prompt
        self.command_for_break = command_for_break
        self.command_parser = command_parser
        self.completer = completer
        self.command_handler = command_handler
        self.__placeholder = placeholder
        # self.__single = single
        self.__required = required
        self.ignore_empty_command = ignore_empty_command
        self.post_handlers = post_handlers

    @property
    def command_prompt(self):
        return f"{MAIN_PROMPT}{self.__command_prompt}{self.required}"

    @property
    def required(self):
        return " (*) " if self.__required else ""

    @property
    def placeholder(self):
        return to_formatted_text(self.__placeholder, style=("class:italic fg:darkred"))

    @placeholder.setter
    def placeholder(self, value):
        self.__placeholder = value

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        session = PromptSession(
            self.command_prompt,
            complete_while_typing=True,
            enable_history_search=True,
            mouse_support=True,
            placeholder=self.placeholder,
        )

        while True:
            input_text = session.prompt(
                completer=self.completer,
                auto_suggest=AutoSuggestFromHistory(),
            ).strip()

            if len(input_text) == 0 and self.ignore_empty_command:
                continue

            if input_text in self.command_for_break and not self.__required:
                break

            command, *args = self.command_parser(input_text)  # maybe **kwargs not now

            if self.command_handler.get(command):
                if all(args):
                    result = self.command_handler[command](*args)
                else:
                    result = self.command_handler[command]()
            else:
                result = get_error_message(f"Unknown command : {command}")

            if result == "#####break####":
                break

            if not (result is None or not result):
                print(result)

            # do post
            if isinstance(self.post_handlers, list):
                for post_handler in self.post_handlers:
                    if callable(post_handler):
                        post_handler()


def break_prompt():
    return "#####break####"
