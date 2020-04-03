import numpy as np
from _mcts import NODE_TREE_DICT


def search_best_node(children_list):
    best_child = None
    best_score = np.float('-inf')
    j = None
    for i, child in enumerate(children_list):
        child_score = child['score']
        if child_score >= best_score:
            best_score = child_score
            best_child = child
            j = i

    return best_child, j


def search():
    global NODE_TREE_DICT
    node_tree = NODE_TREE_DICT.copy()
    node_path = []
    children = 'children'
    while True:
        try:
            node_tree['n'] += 1
            children_list = node_tree[children]
        except KeyError:
            return node_tree, node_path  # if key error return current node
        node_tree, j = search_best_node(children_list)
        node_path.append((children, j))

    return node_tree, node_path

