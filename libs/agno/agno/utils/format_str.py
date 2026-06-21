"""String formatting helpers.

Currently exposes :func:`remove_indent` for stripping leading/trailing
whitespace from every line of a multi-line string, which is useful when
cleaning up triple-quoted prompt templates that were indented for
readability in source code.
"""

from typing import Optional


def remove_indent(s: Optional[str]) -> Optional[str]:
    """Strip leading and trailing whitespace from every line in a string.

    Useful for normalising triple-quoted string literals that carry
    indentation from their surrounding code block.

    Args:
        s: The string to process.  If ``None`` or not a ``str``, returns
            ``None`` unchanged.

    Returns:
        A new string where each line has been stripped of surrounding
        whitespace, joined back with ``"\\n"``.  Returns ``None`` if *s* is
        ``None`` or not a string.

    Example::

        remove_indent("""
            Hello
            World
        """)  # "\\nHello\\nWorld\\n"
    """
    if s is not None and isinstance(s, str):
        return "\n".join([line.strip() for line in s.split("\n")])
    return None
