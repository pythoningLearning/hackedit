import copy


class Copyable:
    def copy(self):
        """
        Returns a copy of the configuration that can be changed without altering this instance.
        """
        return copy.deepcopy(self)