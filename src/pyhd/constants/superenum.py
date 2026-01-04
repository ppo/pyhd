from enum import Enum
from typing import Any


class SuperEnum(Enum):
    """
    Enhanced `Enum` base class supporting multiple named fields per member, aliases, and
    value-based aliases (based on index or a custom field).

    This changes the default behavior regarding `name` and `value` to:
    - `name` is the first found in:
        - The value returned by any custom `_name` property.
        - The first field from `__NAME_FIELD_PRIORITIES__` that is defined.
          (If `__FIELDS__` is not defined, a `name` field is auto-created.)
        - The value of the first custom field.
    - `_key` is the original `name`. Note: Leading `_` to not clash with potential custom field.
    - `value` keeps its original behavior.

    Subclasses should define these if and as needed:
    - `__FIELDS__`: Tuple of field names corresponding to the value tuple.
    - `__ALIASES__`: Dict mapping alias names to member names (`{"alias": " member"}`).
    - `__NUMBERED__`: Bool whether to add a `num` field (one-based). Auto-used as `__VALUE_ALIASES_FIELD__`.
    - `__INDEXED__`: Bool whether to define value-based aliases using members' index (zero-based).
    - `__VALUE_ALIASES_FIELD__`: Name of the field to use for value-based aliases (get via `Enum(x)`).
    """

    # Priority list for fields to be used as `name` value.
    __NAME_FIELD_PRIORITIES__ = ("name", "title")

    # Subclasses must override these – if/as needed.
    __FIELDS__ = ()
    __ALIASES__ = {}
    __NUMBERED__ = False
    __INDEXED__ = False
    __VALUE_ALIASES_FIELD__ = None

    def __init__(self, *args):
        """Initialize `Enum` member by mapping positional arguments to named fields.

        Args are mapped to field names defined in `__FIELDS__`, then stored in `self._kwargs` for
        attribute-style access.
        """
        cls = self.__class__
        self._is_initialized = False  # See `self.index()`.

        # Map positional args to named fields.
        self._kwargs = {}
        if cls.__FIELDS__:
            # Validation
            if len(args) != len(cls.__FIELDS__):
                raise ValueError(
                    f"{cls.__name__}.__FIELDS__ configures {len(cls.__FIELDS__)} fields "
                    f"but {self._name_} provides {len(args)} values."
                )

            # Create mapping.
            for i, value in enumerate(args):
                key = cls.__FIELDS__[i]
                self._kwargs[key] = value
        else:
            self._kwargs["name"] = args[0]

        # Add member aliases.
        for alias, member in cls.__ALIASES__.items():
            if member == self._name_:
                self._add_alias_(alias)

        if cls.__NUMBERED__:
            self._kwargs["num"] = self.index + 1
            if not cls.__FIELDS__ or "name" not in cls.__FIELDS__:
                self._kwargs["name"] = str(self._kwargs["num"])
            cls.__VALUE_ALIASES_FIELD__ = "num"

        # Add value-based aliases based on member's index.
        if cls.__INDEXED__:
            self._add_value_alias_(self.index)

        # Add value-based aliases based on a custom field.
        if cls.__VALUE_ALIASES_FIELD__:
            self._add_value_alias_(getattr(self, cls.__VALUE_ALIASES_FIELD__))

        self._is_initialized = True

    def __str__(self) -> str:
        """Return the name."""
        return self.name

    def __repr__(self) -> str:
        """Return the string used for `repr()` calls."""
        return f"<{self.__class__.__name__}.{self._name_}>"

    def __getattr__(self, key):
        """Enable dot-notation access to named fields.

        Only called when normal attribute lookup fails.
        """
        # Avoid recursion by using object's `__getattribute__`.
        kwargs = object.__getattribute__(self, "_kwargs")
        if key in kwargs:
            return kwargs[key]
        raise AttributeError(f"'{self.__class__.__name__}' has no field '{key}'.")

    def __lt__(self, other):
        """Return whether this should come before `other` when sorting."""
        if isinstance(other, type(self)):
            if "num" in self._kwargs:
                return self.num < other.num
            return self.name < other.name

        if isinstance(other, str):
            return self.name < other

        if isinstance(other, (int, float)):
            return self.num < other

        return NotImplemented

    @property
    def _key(self) -> str:
        """Return the member's key (`Enum`'s `name`)."""
        return self._name_

    @property
    def name(self) -> str:
        """Return `Enum`'s `value` – or equivalent with custom fields."""
        if hasattr(self, "_name"):
            return self._name

        # Note: If `__FIELDS__` is not defined, `name` is auto-created in `_kwargs`.
        for key in self.__NAME_FIELD_PRIORITIES__:
            if key in self._kwargs:
                return str(self._kwargs[key])

        key = self.__FIELDS__[0]
        return str(self._kwargs[key])

    @property
    def full_name(self) -> str:
        if hasattr(self, "title") and self.title != self.name:
            return f"{self.name}: {self.title}"
        return self.name

    @property
    def index(self) -> int:
        """Return zero-based position of this member in the `Enum`."""
        # TODO: The index never changes, should be cached after initialization. How?
        if self._is_initialized:
            return list(self.__class__).index(self)
        return len(list(self.__class__))

    @property
    def fields(self) -> dict:
        """Return a dict with the custom fields and their value."""
        return self._kwargs

    @classmethod
    def get_by_value(cls, value: object, key: str = "name") -> Any:
        """Return a list of all members."""
        for member in cls:
            if getattr(member, key) == value:
                return member
        return None

    @classmethod
    def items(cls) -> tuple["SuperEnum"]:
        """Return a list of all members."""
        return tuple(cls)
