from typing import Any, List


class ResponseIterator:
    """Simple FIFO iterator that buffers items added via `add()` and yields them in insertion order."""

    def __init__(self) -> None:
        self.items: List[Any] = []
        self.index: int = 0

    def add(self, item: Any) -> None:
        """Append an item to the end of the buffer."""
        self.items.append(item)

    def __iter__(self) -> "ResponseIterator":
        return self

    def __next__(self) -> Any:
        if self.index >= len(self.items):
            raise StopIteration
        item = self.items[self.index]
        self.index += 1
        return item
