import re
from typing import Iterable


class C:
    RESET     = "\33[0m"
    BOLD      = "\33[1m"
    BLACK     = "\33[30m"
    RED       = "\33[31m"
    GREEN     = "\33[32m"
    YELLOW    = "\33[33m"
    BLUE      = "\33[34m"
    MAGENTA   = "\33[35m"
    CYAN      = "\33[36m"
    WHITE     = "\33[37m"
    DARK_GRAY = "\33[90m"

    H1      = "\33[1;33m"  # Bold Yellow
    H2      = "\33[1;37m"  # Bold White
    SUCCESS = "\33[32m"    # Green
    FAILURE = "\33[31m"    # Red
    KEY     = "\33[0m"     # Gray (default)
    VALUE   = "\33[36m"    # Cyan
    DIM     = "\33[90m"    # Dark gray
    BORDER  = "\33[90m"    # Dark gray
    LI_NUM  = "\33[90m"    # Dark gray


def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M%z")


def get_indent(indent):
    return "  " * indent

def cprint(color, message, indent=0, end="\n"):
    prefix = get_indent(indent)
    print(f"{color}{prefix}{message}{C.RESET}", end=end)


def print_h1(message, indent=0, lines=False, end="\n"):
    if lines:
        message = f"=== {message} ==="
    print()
    cprint(C.H1, message, indent=indent, end=end)


def print_h2(message, indent=0, lines=False, end="\n"):
    if lines:
        message = f"--- {message} ---"
    # print()
    cprint(C.H2, message, indent=indent, end=end)


def print_dim(message, indent=0, end="\n"):
    cprint(C.DIM, message, indent=indent, end=end)


def print_key(k, indent=0, end="\n"):
    prefix = get_indent(indent)
    print(f"{prefix}{C.KEY}{k}:{C.RESET}", end=end)


def print_value(v, indent=0, end="\n"):
    prefix = get_indent(indent)
    print(f"{prefix}{C.VALUE}{v}{C.RESET}", end=end)


def print_kv(k, v, indent=0, end="\n"):
    prefix = get_indent(indent)
    print(f"{prefix}{C.KEY}{k}: {C.VALUE}{v}{C.RESET}", end=end)


def print_csv_list(k, items, indent=0, end="\n"):
    print_kv(k, ", ".join(items), indent=indent, end=end)


def print_num_list(k, items, indent=0):
    if k:
        print_key(k, indent=indent, end=" ")
        print_dim(f"({len(items)})")
    pad = len(str(len(items)))
    for i, item in enumerate(items):
        print_kv(f"{C.LI_NUM}{i+1:>{pad}}", item, indent=indent+1)


def print_table(
    data: Iterable[Iterable[str]],
    header_rows: int = 1,
    header_cols: int = 1,
    formats: Iterable[str] = None,
) -> None:
    """."""

    # Initialize formats.
    if formats is None:
        formats = [None for _ in data[0]]

    # Make sure rows & cols are lists, and all columns are strings.
    data = list(data)
    for r, row in enumerate(data):
        data[r] = [str(col) for col in row]

    # Find max width for each column.
    widths = [0 for _ in data[0]]  # Initialize columns width.
    for row in data:
        widths = [max(len(col), widths[c]) for c, col in enumerate(row)]

    # Initialize formats.
    formats = [
        None if f is None else f.replace("w", str(widths[c]))
        for c, f in enumerate(formats)
    ]

    # Insert header separator row.
    if header_rows > 0:
        data.insert(header_rows, [f"{C.BORDER}{'-' * w}{C.RESET}" for w in widths])
        header_rows += 1

    # Process rows.
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            w = widths[c]  # Width of this column.
            f = formats[c]
            color = (C.KEY if r < header_rows or c < header_cols
                     else C.VALUE)

            if r >= header_rows and f:  # Handle column with formatting (not in header).
                s = f"{col:{f}}"
            else:
                s = f"{col:{w}}"

            print(f"{C.BORDER}| {color}{s}{C.RESET} ", end="")  # Print column (with left border).

        cprint(C.BORDER, "|")  # Print table right border.
