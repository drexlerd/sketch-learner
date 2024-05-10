


class KeyToInt:
    def __init__(self):
        self._key_to_int = dict()

    def get_int_from_key(self, key: str):
        if key not in self._key_to_int:
            self._key_to_int[key] = len(self._key_to_int)
        return self._key_to_int[key]

    def size(self) -> int:
        return len(self._key_to_int)
