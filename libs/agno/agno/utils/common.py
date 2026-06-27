from dataclasses import asdict
from typing import Any, Dict, List, Optional, Set, Type, Union, get_type_hints


def isinstanceany(obj: Any, class_list: List[Type]) -> bool:
    """Return True if obj is an instance of any class in class_list.

    Args:
        obj: The object to check.
        class_list: A list of types to check against.

    Returns:
        True if obj is an instance of at least one class in class_list,
        False otherwise.
    """
    for cls in class_list:
        if isinstance(obj, cls):
            return True
    return False


def is_empty(val: Any) -> bool:
    """Return True if val is None, an empty string, or a zero-length sequence.

    Args:
        val: The value to check.

    Returns:
        True if val is considered empty, False otherwise.
    """
    if val is None or val == "":
        return True
    try:
        return len(val) == 0
    except TypeError:
        return False


def get_image_str(repo: str, tag: str) -> str:
    """Return a Docker-style image string in the form ``repo:tag``.

    Args:
        repo: The image repository name (e.g. ``"myorg/myimage"``).
        tag: The image tag (e.g. ``"latest"`` or ``"1.2.3"``).

    Returns:
        A string of the form ``"<repo>:<tag>"``.
    """
    return f"{repo}:{tag}"


def dataclass_to_dict(
    dataclass_object: Any,
    exclude: Optional[Set[str]] = None,
    exclude_none: bool = False,
) -> Dict[str, Any]:
    """Convert a dataclass instance to a plain dictionary.

    Args:
        dataclass_object: An instance of a Python dataclass.
        exclude: An optional set of field names to omit from the result.
        exclude_none: If True, fields whose value is None are omitted.

    Returns:
        A dictionary representation of the dataclass.
    """
    final_dict: Dict[str, Any] = asdict(dataclass_object)
    if exclude:
        for key in exclude:
            final_dict.pop(key, None)
    if exclude_none:
        final_dict = {k: v for k, v in final_dict.items() if v is not None}
    return final_dict


def nested_model_dump(value: Any) -> Any:
    """Recursively convert Pydantic models, dicts, and lists to plain Python objects.

    Pydantic ``BaseModel`` instances are converted via ``model_dump()``.
    Dicts and lists are traversed recursively.  All other values are
    returned unchanged.

    Args:
        value: The value to convert.

    Returns:
        A plain Python object (dict, list, or scalar) with no Pydantic models.
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
    """Return True if *cls* is a TypedDict class.

    The check relies on the presence of the dunder attributes that the
    ``typing.TypedDict`` machinery injects at class creation time.

    Args:
        cls: The class to inspect.

    Returns:
        True if cls was created with ``TypedDict``, False otherwise.
    """
    return (
        hasattr(cls, "__annotations__")
        and hasattr(cls, "__total__")
        and hasattr(cls, "__required_keys__")
        and hasattr(cls, "__optional_keys__")
    )


def check_type_compatibility(value: Any, expected_type: Type[Any]) -> bool:
    """Return True if *value* is compatible with *expected_type*.

    Handles ``Optional``, ``Union``, and parameterised ``List`` types in
    addition to plain built-in types.  Falls back to ``True`` for
    complex generic types that cannot be checked at runtime.

    Args:
        value: The value to validate.
        expected_type: The type annotation to validate against.

    Returns:
        True if the value is compatible with the expected type,
        False if a definitive incompatibility is detected.
    """
    from typing import get_args, get_origin

    # Handle None / Optional types
    if value is None:
        return (
            type(None) in get_args(expected_type)
            if hasattr(expected_type, "__args__")
            else expected_type is type(None)
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
        # Generic aliases (e.g. Dict[str, Any]) cannot be used with isinstance
        return True


def validate_typed_dict(data: Dict[str, Any], schema_cls: Type[Any]) -> Dict[str, Any]:
    """Validate *data* against a TypedDict *schema_cls* and return a clean copy.

    Checks that all required keys are present, no unexpected keys exist, and
    that each value passes a basic type-compatibility check.

    Args:
        data: The input dictionary to validate.
        schema_cls: A ``TypedDict`` class that defines the expected schema.

    Returns:
        A validated copy of *data* containing only the keys declared in
        *schema_cls*.

    Raises:
        ValueError: If *data* is not a dict, required fields are missing,
            unexpected fields are present, or a value fails its type check.
    """
    if not isinstance(data, dict):
        raise ValueError(f"Expected dict for TypedDict {schema_cls.__name__}, got {type(data)}")

    # Resolve type hints (handles forward references)
    try:
        type_hints: Dict[str, Any] = get_type_hints(schema_cls)
    except Exception as exc:
        raise ValueError(
            f"Could not get type hints for TypedDict {schema_cls.__name__}: {exc}"
        ) from exc

    required_keys: Set[str] = getattr(schema_cls, "__required_keys__", set())
    optional_keys: Set[str] = getattr(schema_cls, "__optional_keys__", set())
    all_keys: Set[str] = required_keys | optional_keys

    missing_required = required_keys - set(data.keys())
    if missing_required:
        raise ValueError(
            f"Missing required fields in TypedDict {schema_cls.__name__}: {missing_required}"
        )

    unexpected_fields = set(data.keys()) - all_keys
    if unexpected_fields:
        raise ValueError(
            f"Unexpected fields in TypedDict {schema_cls.__name__}: {unexpected_fields}"
        )

    validated_data: Dict[str, Any] = {}
    for field_name, value in data.items():
        if field_name in type_hints:
            expected_type = type_hints[field_name]
            if not check_type_compatibility(value, expected_type):
                raise ValueError(
                    f"Field '{field_name}' expected type {expected_type}, "
                    f"got {type(value)} with value {value}"
                )
            validated_data[field_name] = value

    return validated_data
