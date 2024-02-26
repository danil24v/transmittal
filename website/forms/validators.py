import re


class FormValidator():

    def validate(self, value) -> str:
        return "Error! Def validation!"


class RegexpValidator(FormValidator):
    def __init__(self, regexp, allow_empty=False):
        self._regexp = regexp
        self._allow_empty = allow_empty

    def validate(self, value) -> bool:
        if len(value.strip()) == 0 and self._allow_empty:
            return True
        return re.match(self._regexp, value)


class MutliLineValidator(FormValidator):

    def __init__(self, regexp: str, max_size: int, allow_empty: bool):
        self._regexp = regexp
        self._max_size = max_size
        self._allow_empty = allow_empty

    def validate(self, value) -> bool:
        lines = value.split('\n')
        size = len(value)
        result = True

        for line in lines:
            line_len = len(line)
            if line_len < self._min_line or line_len > self._max_line:
                return False
            if not re.match(self._regexp, line):
                result = False
                break

        return result
