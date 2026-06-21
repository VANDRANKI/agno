"""Dictionary merge utilities for combining agent session state.

Provides two merge strategies:

- :func:`merge_dictionaries` — a standard recursive (deep) merge where
  values from the second dict overwrite matching keys in the first.
- :func:`merge_parallel_session_states` — a change-aware merge designed
  for parallel agent steps: only keys whose values actually changed from
  the original state are applied, preventing steps from silently
  overwriting each other's updates.
"""

from typing import Any, Dict, List


def merge_dictionaries(a: Dict[str, Any], b: Dict[str, Any]) -> None:
    """Recursively merge *b* into *a* in place (deep merge).

    For every key in *b*:

    - If the key exists in *a* and both values are dicts, the sub-dicts are
      merged recursively.
    - Otherwise the value from *b* overwrites the value in *a*.

    Args:
        a: The target dictionary, modified in place.
        b: The source dictionary whose values take precedence on conflicts.

    Returns:
        None — *a* is modified in place.

    Example::

        a = {"x": 1, "nested": {"y": 2}}
        b = {"nested": {"z": 3}, "w": 4}
        merge_dictionaries(a, b)
        # a == {"x": 1, "nested": {"y": 2, "z": 3}, "w": 4}
    """
    for key in b:
        if key in a and isinstance(a[key], dict) and isinstance(b[key], dict):
            merge_dictionaries(a[key], b[key])
        else:
            a[key] = b[key]


def merge_parallel_session_states(original_state: Dict[str, Any], modified_states: List[Dict[str, Any]]) -> None:
    """Merge the results of parallel agent steps back into the original session state.

    Unlike a plain dict update, this function only applies keys that were
    *actually changed* by a parallel step (i.e. keys whose value differs from
    the original state).  This prevents a step that echoes unchanged keys from
    silently overwriting updates made by a sibling step.

    When two parallel steps modify the *same* key, the last step in
    *modified_states* wins (last-write-wins semantics).

    Args:
        original_state: The session state dict recorded *before* the parallel
            steps ran.  Modified in place with all collected changes.
        modified_states: A list of session state dicts, one per completed
            parallel step.  Each dict represents the full session state after
            that step finished.

    Returns:
        None — *original_state* is modified in place.

    Note:
        If *original_state* or *modified_states* is falsy (empty dict /
        empty list), the function returns immediately without modifying
        anything.
    """
    if not original_state or not modified_states:
        return

    # Collect all actual changes (keys where the value differs from the original)
    all_changes: Dict[str, Any] = {}
    for modified_state in modified_states:
        if modified_state:
            for key, value in modified_state.items():
                if key not in original_state or original_state[key] != value:
                    all_changes[key] = value

    # Apply all collected changes to the original state
    for key, value in all_changes.items():
        original_state[key] = value
