from typing import Generic, List, TypeVar

T = TypeVar("T")


class ResponseIterator(Generic[T]):
    """A simple forward-only iterator that yields previously added items in insertion order."""

    def __init__(self) -> None:
        self.items: List[T] = []
        self.index: int = 0

    def add(self, item: T) -> None:
        self.items.append(item)

    def __iter__(self) -> "ResponseIterator[T]":
        return self

    def __next__(self) -> T:
        if self.index >= len(self.items):
            raise StopIteration
        item = self.items[self.index]
        self.index += 1
        return item
