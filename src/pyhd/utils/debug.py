import dataclasses
import json
from datetime import date, datetime, time
from types import MappingProxyType

from ..constants.superenum import SuperEnum
from .display import (
    get_indent,
    print_csv_list,
    print_dim,
    print_h1,
    print_h2,
    print_key,
    print_kv,
    print_num_list,
    print_value,
)


def jsonify(obj):
    if hasattr(obj, "to_dict") and callable(obj.to_dict):
        return jsonify(obj.to_dict())
    if isinstance(obj, (str, float, int, bool, type(None))):
        return obj
    if isinstance(obj, (dict, MappingProxyType)):
        return {jsonify(k): jsonify(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return list(jsonify(i) for i in obj)
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    if dataclasses.is_dataclass(obj):
        # return jsonify(dataclasses.asdict(obj))
        return {field.name: jsonify(getattr(obj, field.name)) for field in dataclasses.fields(obj)}
    # if isinstance(obj, SuperEnum):
    #     return debug_superenum(obj)
    # if hasattr(obj, "__dict__"):
    #     return jsonify(vars(obj))
    return repr(obj)


def debug(value: object, label: str = None, output: bool = True) -> str:
    count = len(value) if isinstance(value, (list, tuple, set, dict)) else None
    output_str = ""

    if label:
        output_str += str(label)
        if count is not None:
            output_str += f" ({count})"
        output_str += ": "

    output_str += json.dumps(jsonify(value), indent=2, ensure_ascii=False)

    if output:
        print(output_str)

    return output_str


def debug_superenum(obj: object, compact: bool = False) -> None:
    indent = 0

    if not isinstance(obj, SuperEnum):
        # ENUM
        print_h1("SuperEnum:", indent=indent, end=" ")
        print_value(obj.__name__)

        indent += 1
        for k in ("FIELDS", "ALIASES"):
            v = getattr(obj, f"__{k}__")
            if v:
                print_csv_list(k, v, indent=indent)

        for k in ("VALUE_ALIASES_FIELD", "NUMBERED", "INDEXED"):
            v = getattr(obj, f"__{k}__")
            if v:
                print_kv(k, v, indent=indent)
        indent -= 1

        # ALL ITEMS
        items = obj.items()
        num_items = len(items)
        print_h1(f"{obj.__name__} Items:", indent=indent, end=" ")
        print_dim(f"({num_items})")
        limited = compact and len(items) > 5
        if limited:
            items = items[:5]
            num_items = len(items)

        num_digits = len(str(abs(num_items)))
        indent += 1
        for i, item in enumerate(items):
            print_dim(f"{i+1:>{num_digits}}.", indent=indent, end=" ")
            print_key(item._key, end=" ")
            print_value(item.full_name)
        if limited:
            print_dim(f"{get_indent(indent)}…")
        indent -= 1

        # Simulate instance
        obj = obj.items()[0]

    # INSTANCE
    print_h1("Instance:", end=" ")
    print_value(repr(obj))
    indent += 1
    print_kv("_key", obj._key, indent=indent)
    print_kv("index", obj.index, indent=indent)
    # print_kv("str", str(obj), indent=indent)
    if hasattr(obj, "num"):
        print_kv("num", obj.num, indent=indent)
    print_kv("name", obj.name, indent=indent)
    if obj.full_name and obj.full_name != obj.name:
        print_kv("full_name", obj.full_name, indent=indent)

    ## Fields
    fields = {k: v for k, v in obj.fields.items() if k not in ("name", "num")}
    if fields:
        print_h2("Fields:", indent=indent)
        indent += 1
        for k, v in fields.items():
            print_kv(k, v, indent=indent)
        indent -= 1

    EXCLUDED_MEMBERS = (
        "__class__", "__doc__", "__eq__", "__hash__", "__module__",
        "_key", "fields", "full_name", "index", "name", "value",
        "get_by_value", "items",
    )
    obj_members = [name for name in dir(obj) if name not in EXCLUDED_MEMBERS]

    ## Props
    custom_props = [name for name in obj_members if not callable(getattr(obj, name))]
    if custom_props:
        print_h2("Props:", indent=indent)
        indent += 1
        for name in custom_props:
            value = getattr(obj, name)

            if isinstance(value, (tuple, list)):
                if compact and len(value) > 5:
                    print_num_list(name, value[:5], indent=indent)
                    print_dim("…", indent=indent)
                else:
                    print_num_list(name, value, indent=indent)
            else:
                print_kv(name, value, indent=indent)

            # if compact and isinstance(value, tuple) and len(value) > 5:
            #     value = f"({len(value)} <{value[0].__class__.__name__}>…)"
            # print_kv(name, value, indent=indent)
        indent -= 1

    ## Methods
    custom_methods = [name for name in obj_members if callable(getattr(obj, name))]
    if custom_methods:
        print_h2("Methods:", indent=indent)
        indent += 1
        prefix = get_indent(indent)
        for name in custom_methods:
            print(f"{prefix}{name}()")
        indent -= 1

    indent -= 1
