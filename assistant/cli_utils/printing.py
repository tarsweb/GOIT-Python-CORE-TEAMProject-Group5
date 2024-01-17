from typing import ClassVar
from collections.abc import Iterable

from prettytable.colortable import ColorTable, Theme


def print_records(records: [ClassVar], color: str = "34") -> ColorTable:
    pt = ColorTable(
        theme=Theme(default_color=color),
        border=True,
        header=True,
        padding_width=2,
        header_style="upper",
    )

    pt.field_names = records[0].__dict__.keys()

    for record in records:
        row_array = []
        for field_name in pt.field_names:
            class_atr = getattr(record, field_name)
            if isinstance(class_atr, Iterable):
                if isinstance(class_atr, str):
                    row_array.append(class_atr)
                else:
                    atr_array = [str(el) for el in class_atr]
                    row_array.append(", ".join(atr_array))
            else:
                row_array.append(str(class_atr))
        pt.add_row(row_array)

    pt.align = "c"
    pt.align["name"] = "l"
    pt.align["phones"] = "l"

    return pt


def print_clear_folder(records: [dict]) -> ColorTable:
    pt = ColorTable(
        theme=Theme(default_color="34"),
        border=True,
        header=True,
        padding_width=2,
        header_style="upper",
    )

    pt.field_names = ["type", "files"]

    for record in records:
        row_array = []
        for key, value in record.items():
            row_array.append(key)
            row_array.append(value)
        pt.add_row(row_array)

    pt.align = "l"

    return pt
