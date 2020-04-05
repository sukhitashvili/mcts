from functools import reduce


def get_func(obj, key):
    return obj.__getitem__(key)


def get_value_by_path(container, path):
    return reduce(get_func, path, container)


def set_value_by_path(container, path, value):
    obj = reduce(get_func, path[:-1], container)
    obj.__setitem__(path[-1], value)
    return container
