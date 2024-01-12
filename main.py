from cli_utils import register, listener, show_register_command
import addressbook


@register("hello")
def hello() -> str:
    return "How can I help you?"

@register("add")
def add(num: int ) -> int:
    if not isinstance(num, int):
        try:
            num = int(num)
        except ValueError :
            num = 0

    return num * 2

if __name__ == "__main__":
    addressbook.initialize()
    print(show_register_command())
    listener()
