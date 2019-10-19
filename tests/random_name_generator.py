from pathlib import Path
from typing import Dict, Iterable, Any
import toml
from mentormatch.utils.enums import Gender


class RandomNameGenerator:

    def __init__(self):
        path = Path(__file__).parent / "files" / 'names.toml'
        names: Dict = toml.load(path)
        self._names = dict()
        self._names['last'] = _infinite_list_looper(names['last_names'])
        self._names['first'] = {
            Gender.MALE: _infinite_list_looper(names['first_names_male']),
            Gender.FEMALE: _infinite_list_looper(names['first_names_female']),
        }

    def get_first_name(self, gender: Gender) -> str:
        return next(self._names['first'][gender])

    def get_last_name(self) -> str:
        return next(self._names['last'])


def _infinite_list_looper(_iterable: Iterable) -> Any:
    while True:
        yield from _iterable
        continue


if __name__ == '__main__':
    pass
    # looper = _infinite_list_looper(range(3))
    # for i in range(10):
    #     print(next(looper))

    # for gender in Gender:
    #     print(gender.lower())
    #     print(gender.name)