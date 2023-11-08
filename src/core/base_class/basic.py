import abc
import functools


class Basic:

    @abc.abstractmethod
    def cmp(self, other):
        pass


def cmp(main: Basic, other: Basic) -> int:
    self_type = id(type(main))
    other_type = id(type(other))

    if self_type != other_type:
        return self_type - other_type

    return main.cmp(other)


def sorted_basics(basics: list[Basic]) -> list[Basic]:
    return sorted(basics, key=functools.cmp_to_key(cmp))


def sorted_list_basics(main: list[Basic], other: list[Basic]) -> int:
    main_len = len(main)
    other_len = len(other)

    if main_len != other_len:
        return main_len - other_len

    for main_item, other_item in zip(main, other):

        x = cmp(main_item, other_item)
        if x != 0:
            return x

    return 0
