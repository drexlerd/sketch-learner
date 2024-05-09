


class KeyToInt:
    def __init__(self):
        self._key_to_color = dict()

    def get_int_from_key(self, key):
        if key not in self._key_to_color:
            self._key_to_color[key] = len(self._key_to_color)
        return self._key_to_color[key]
