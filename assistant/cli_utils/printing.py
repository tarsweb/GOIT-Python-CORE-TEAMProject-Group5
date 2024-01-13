from typing import ClassVar
from collections.abc import Iterable

from prettytable.colortable import ColorTable, Theme


def print_records(records: [ClassVar]) -> None:
    pt = ColorTable(
        theme=Theme(default_color="34"),
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
                atr_array = [str(el) for el in class_atr]
                row_array.append(", ".join(atr_array))
            else:
                row_array.append(str(class_atr))
        pt.add_row(row_array)

    pt.align = "c"
    pt.align["name"] = "l"
    pt.align["phones"] = "l"
    print(pt)
