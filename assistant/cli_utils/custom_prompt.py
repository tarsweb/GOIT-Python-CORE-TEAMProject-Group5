from typing import Any
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from .utils import COMMAND_PROMPT

class CustomPrompt:
    def __init__(
        self,
        command_prompt: str,
        completer: Completer,
        command_for_break: str | tuple,
        command_parser,
        command_handler,
        placeholder: str = "",
    ) -> None:
        self.command_prompt = f"{COMMAND_PROMPT}{command_prompt}"
        self.command_for_break = command_for_break
        self.command_parser = command_parser
        self.completer = completer
        self.command_handler = command_handler
        self.placeholder = placeholder

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        session = PromptSession(
            self.command_prompt,
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
                print(f"Unknown command : {command}")
