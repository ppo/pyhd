"""
TODO.
"""

from typing import Iterable


def filter_list(
    keys: Iterable[str],
    include: Iterable[str] = None,
    exclude: Iterable[str] = None,
) -> Iterable[str]:
    """Return the list of keys filtered using include/exclude lists."""
    if include is not None:
        keys = include
    if exclude is not None:
        keys = [k for k in keys if k not in exclude]
    return keys


def to_dict(
    obj: object | dict,
    keys: Iterable[str],
    include: Iterable[str] = None,
    exclude: Iterable[str] = None,
) -> dict:
    """Export an object as dict, containing only the desired keys."""
    keys = filter_list(keys, include=include, exclude=exclude)

    if hasattr(obj, "get"):
        return {k: obj.get(k) for k in keys}

    return {k: getattr(obj, k) for k in keys}
