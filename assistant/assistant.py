from cli_utils import register, listener, show_register_command
import addressbook
import notes

# Example (приклад)
@register("hello")
def hello() -> str:
    return "How can I help you?"

# Example (приклад)
@register("add")
def add(num: int) -> int:
    if not isinstance(num, int):
        try:
            num = int(num)
        except ValueError:
            num = 0

    return num * 2


def main():
    addressbook.initialize()
    notes.initialize()
    print(show_register_command())
    listener()


if __name__ == "__main__":
    main()
