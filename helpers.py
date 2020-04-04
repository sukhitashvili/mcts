from functools import reduce
from copy import deepcopy


def check_tree_depth(tree):
    depth = 1
    t = deepcopy(tree)
    for i in range(500):
        try:
            c_l = t['children']
            no_child = 1
            for c in c_l:
                if 'children' in c.keys():
                    t = deepcopy(c)
                    no_child = 0
                    break
            if no_child:
                break
            depth += 1
        except:
            break
    return depth


def get_func(obj, key):
    return obj.__getitem__(key)


def get_value_by_path(container, path):
    return reduce(get_func, path, container)


def set_value_by_path(container, path, value):
    obj = reduce(get_func, path[:-1], container)
    obj.__setitem__(path[-1], value)
    return container


if __name__ == '__main__':
    d = {'a': 666,
         'children': [
             {'b': 666,
              'children': [
                  {'a': 666,
                   'children': [
                       {'c': 666,
                        'children': [
                            {'a': 777}
                        ]},
                       {'r': 666}
                   ]},
                  {'A': 777}
              ],
              'n': 0},
             {'c': 666}
         ],
         'n': 0}
    # print((check_tree_depth(d)))
    path = ['children'] + [0] + ['n']
    print(set_value_by_path(d, path, get_value_by_path(d, path) + 1))
