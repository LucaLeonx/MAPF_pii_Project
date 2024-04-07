from optional import Optional


class EntityDescription:
    def __init__(self, name, start_position=None):
        if name != "":
            self._name = name
        else:
            raise ValueError("Entity Name cannot be empty")

        self._start_position = Optional.of(start_position)

    def get_name(self):
        return self._name

    def get_start_position(self):
        return self._start_position

    def has_start_position(self):
        return self._start_position.is_present()


# Will be moved later if additional methods will be added




