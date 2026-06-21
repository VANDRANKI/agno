"""General-purpose utility helpers used throughout the agno library.

This module collects small, stateless helpers that do not fit neatly into
a more specific utility module.  It is intentionally kept dependency-light
(only stdlib + pydantic) so it can be imported early without triggering
heavy optional dependencies.

Categories
----------
- Type checking: :func:`isinstanceany`, :func:`is_empty`
- Image helpers: :func:`get_image_str`
- Dataclass / Pydantic serialization: :func:`dataclass_to_dict`,
  :func:`nested_model_dump`
- TypedDict inspection and validation: :func:`is_typed_dict`,
  :func:`check_type_compatibility`, :func:`validate_typed_dict`
"""

from dataclasses import asdict
from typing import Any, Dict, List, Optional, Set, Type, Union, get_type_hints


def isinstanceany(obj: Any, class_list: List[Type]) -> bool:
    """Return ``True`` if *obj* is an instance of any class in *class_list*.

    Args:
        obj: The object to test.
        class_list: A list of types to test against.

    Returns:
        ``True`` as soon as a matching type is found; ``False`` otherwise.
    """
    for cls in class_list:
        if isinstance(obj, cls):
            return True
    return False


def is_empty(val: Any) -> bool:
    """Return ``True`` if *val* is ``None``, an empty string, or has length 0.

    Args:
        val: The value to check.

    Returns:
        ``True`` if *val* is considered empty, ``False`` otherwise.
    """
    if val is None or len(val) == 0 or val == "":
        return True
    return False


def get_image_str(repo: str, tag: str) -> str:
    """Build a fully-qualified Docker image reference string.

    Args:
        repo: The image repository path (e.g. ``"myorg/myimage"``).
        tag: The image tag (e.g. ``"latest"`` or ``"1.2.3"``).

    Returns:
        A colon-joined ``"<repo>:<tag>"`` string suitable for use in
        ``docker pull`` or container runtime APIs.

    Example::

        get_image_str("myorg/myimage", "1.2.3")  # "myorg/myimage:1.2.3"
    """
    return f"{repo}:{tag}"


def dataclass_to_dict(dataclass_object: Any, exclude: Optional[set[str]] = None, exclude_none: bool = False) -> Dict[str, Any]:
    """Convert a dataclass instance to a plain dictionary.

    Args:
        dataclass_object: A dataclass instance to serialize.
        exclude: Optional set of top-level field names to omit from the
            returned dict.
        exclude_none: If ``True``, fields whose value is ``None`` are removed.

    Returns:
        A (possibly filtered) dict representation of *dataclass_object*.
    """
    final_dict = asdict(dataclass_object)
    if exclude:
        for key in exclude:
            final_dict.pop(key, None)
    if exclude_none:
        final_dict = {k: v for k, v in final_dict.items() if v is not None}
    return final_dict


def nested_model_dump(value: Any) -> Any:
    """Recursively serialize Pydantic models and nested containers to plain Python objects.

    Pydantic ``BaseModel`` instances are converted via ``model_dump()``.  Dicts
    and lists are traversed recursively so that models nested at any depth are
    also converted.  All other values (str, int, float, None, …) are returned
    unchanged.

    Args:
        value: The value to serialize.  May be a :class:`pydantic.BaseModel`,
            a ``dict``, a ``list``, or any other Python object.

    Returns:
        A plain Python object with no remaining Pydantic model instances.

    Example::

        class Inner(BaseModel):
            x: int

        class Outer(BaseModel):
            inner: Inner

        nested_model_dump(Outer(inner=Inner(x=1)))  # {"inner": {"x": 1}}
    """
    from pydantic import BaseModel

    if isinstance(value, BaseModel):
        return value.model_dump()
    elif isinstance(value, dict):
        return {k: nested_model_dump(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [nested_model_dump(item) for item in value]
    return value


def is_typed_dict(cls: Type[Any]) -> bool:
    """Return ``True`` if *cls* looks like a :func:`typing.TypedDict` class.

    Uses structural duck-typing: checks for the three dunder attributes that
    every ``TypedDict`` subclass carries (``__annotations__``, ``__total__``,
    ``__required_keys__``, ``__optional_keys__``).

    Args:
        cls: The class to inspect.

    Returns:
        ``True`` if *cls* has all four TypedDict marker attributes.
    """
    return (
        hasattr(cls, "__annotations__")
        and hasattr(cls, "__total__")
        and hasattr(cls, "__required_keys__")
        and hasattr(cls, "__optional_keys__")
    )


def check_type_compatibility(value: Any, expected_type: Type) -> bool:
    """Perform a best-effort runtime type-compatibility check.

    Supports ``None``/``Optional``, ``Union``, ``List[T]``, and concrete
    types such as ``str``, ``int``, ``float``, and ``bool``.  Falls back to
    ``isinstance`` for other types and returns ``True`` on any
    :exc:`TypeError` (e.g. when the expected type is a generic alias that
    ``isinstance`` cannot handle directly).

    Args:
        value: The value whose type is to be checked.
        expected_type: The type annotation to check against.

    Returns:
        ``True`` if *value* is compatible with *expected_type*,
        ``False`` otherwise.
    """
    from typing import get_args, get_origin

    # Handle None / Optional types
    if value is None:
        return (
            type(None) in get_args(expected_type) if hasattr(expected_type, "__args__") else expected_type is type(None)
        )

    # Handle Union types (including Optional)
    origin = get_origin(expected_type)
    if origin is Union:
        return any(check_type_compatibility(value, arg) for arg in get_args(expected_type))

    # Handle List types
    if origin is list or expected_type is list:
        if not isinstance(value, list):
            return False
        if origin is list and get_args(expected_type):
            element_type = get_args(expected_type)[0]
            return all(check_type_compatibility(item, element_type) for item in value)
        return True

    if expected_type in (str, int, float, bool):
        return isinstance(value, expected_type)

    if expected_type is Any:
        return True

    try:
        return isinstance(value, expected_type)
    except TypeError:
        # Generic aliases (e.g. Dict[str, int]) cannot be used with isinstance;
        # treat as compatible and let runtime usage surface any real errors.
        return True


def validate_typed_dict(data: dict, schema_cls: Type[Any]) -> dict:
    """Validate a plain dict against a TypedDict schema.

    Checks that all required keys are present, no unexpected keys appear, and
    each provided value is compatible with its annotated type
    (via :func:`check_type_compatibility`).

    Args:
        data: The dict to validate.
        schema_cls: A :func:`typing.TypedDict` class whose annotations define
            the expected structure.

    Returns:
        A copy of *data* containing only the recognized fields.  Unexpected
        keys are rejected (see below) rather than silently dropped.

    Raises:
        ValueError: If *data* is not a dict, if required fields are missing,
            if unexpected fields are present, if type hints cannot be resolved,
            or if a field value is incompatible with its annotated type.
    """
    if not isinstance(data, dict):
        raise ValueError(f"Expected dict for TypedDict {schema_cls.__name__}, got {type(data)}")

    # Get type hints from the TypedDict
    try:
        type_hints = get_type_hints(schema_cls)
    except Exception as e:
        raise ValueError(f"Could not get type hints for TypedDict {schema_cls.__name__}: {e}")

    # Get required and optional keys
    required_keys: Set[str] = getattr(schema_cls, "__required_keys__", set())
    optional_keys: Set[str] = getattr(schema_cls, "__optional_keys__", set())
    all_keys = required_keys | optional_keys

    # Check for missing required fields
    missing_required = required_keys - set(data.keys())
    if missing_required:
        raise ValueError(f"Missing required fields in TypedDict {schema_cls.__name__}: {missing_required}")

    # Check for unexpected fields
    unexpected_fields = set(data.keys()) - all_keys
    if unexpected_fields:
        raise ValueError(f"Unexpected fields in TypedDict {schema_cls.__name__}: {unexpected_fields}")

    # Basic type checking for provided fields
    validated_data = {}
    for field_name, value in data.items():
        if field_name in type_hints:
            expected_type = type_hints[field_name]

            if not check_type_compatibility(value, expected_type):
                raise ValueError(
                    f"Field '{field_name}' expected type {expected_type}, got {type(value)} with value {value}"
                )

            validated_data[field_name] = value

    return validated_data
