from typing import Optional


class ByteManager:
    """
    Manage Bytes

    === Attributes ===
    _b: bytes | None
    stores data
    """
    _b: Optional[bytes]

    def __init__(self, b: Optional[bytes] = None) -> None:
        self._b = b

    def from_file(self, file_path: str) -> None:
        """
        Load data from file
        """
        with open(file_path, 'rb') as f:
            self._b = f.read()

    def to_integer(self, offset: int, size: int) -> int:
        s = self._b[offset: offset + size]
        return int.from_bytes(s, 'little', signed=False)
