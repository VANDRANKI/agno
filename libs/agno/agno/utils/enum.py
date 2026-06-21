"""Enum utilities providing an extended base class with convenience helpers.

:class:`ExtendedEnum` adds two class methods to the standard
:class:`enum.Enum`:

- :meth:`~ExtendedEnum.values_list` — return all member values as a list.
- :meth:`~ExtendedEnum.from_str` — look up a member by its string value
  (case-sensitive), raising :exc:`NotImplementedError` on a miss.

Example::

    class Color(ExtendedEnum):
        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    Color.values_list()          # ["red", "green", "blue"]
    Color.from_str("red")        # <Color.RED: 'red'>
    Color.from_str("unknown")    # NotImplementedError
"""

from enum import Enum
from typing import Any, List, Optional


class ExtendedEnum(Enum):
    """Enum base class with list and string-lookup helpers."""

    @classmethod
    def values_list(cls) -> List[Any]:
        """Return a list of all member values in definition order.

        Returns:
            A list containing the ``.value`` of every member.

        Example::

            class Status(ExtendedEnum):
                ACTIVE = "active"
                INACTIVE = "inactive"

            Status.values_list()  # ["active", "inactive"]
        """
        return [member.value for member in cls]

    @classmethod
    def from_str(cls, str_to_convert_to_enum: Optional[str]) -> Optional[Any]:
        """Convert a string value to an enum member (case-sensitive).

        Args:
            str_to_convert_to_enum: The string value to look up. ``None``
                is returned unchanged.

        Returns:
            The matching enum member, or ``None`` if the input was ``None``.

        Raises:
            NotImplementedError: If *str_to_convert_to_enum* is not ``None``
                and does not match any member value.

        Example::

            Status.from_str("active")   # <Status.ACTIVE: 'active'>
            Status.from_str(None)       # None
            Status.from_str("ACTIVE")   # NotImplementedError (case-sensitive)
        """
        if str_to_convert_to_enum is None:
            return None

        if str_to_convert_to_enum in cls._value2member_map_:
            return cls._value2member_map_.get(str_to_convert_to_enum)

        raise NotImplementedError(
            f"{str_to_convert_to_enum!r} is not a valid member of {cls.__name__}. "
            f"Valid values are: {list(cls._value2member_map_.keys())}"
        )
