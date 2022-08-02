from typing import Optional


class Key:
    def __init__(
        self, key: str, key_type: Optional[str] = None, index: Optional[str] = None, count: int = 1
    ) -> None:
        self.key = key
        self.key_type = key_type or key
        self.index = index
        self.count = count

    def __str__(self) -> str:
        return self.key

    def __repr__(self) -> str:
        return self.key
