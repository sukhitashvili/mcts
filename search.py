import numpy as np
import copy

C = 2  # exploration factor constant, the higher it is the more exploration is done


def search_best_node(children_list, parent_n):
    best_child = None
    best_score = np.float('-inf')
    j = None
    for i, child in enumerate(children_list):
        child_score = child['total_score']
        child_score += 2 * C * np.sqrt(2 * np.log(parent_n) / child['n'])  # upper confidence bound heuristic
        if child_score >= best_score:
            best_score = child_score
            best_child = child
            j = i

    return best_child, j


def search(node_tree_dict):
    node_tree = copy.deepcopy(node_tree_dict)
    node_path = []
    children = 'children'
    while True:
        try:
            parent_n = node_tree['n']
            children_list = node_tree[children]
            # if node does not have children then 'n' wont be increased!
            node_tree['n'] += 1  # if a node passed take into account that
        except KeyError:
            return node_tree, None  # if key error return current node
        node_tree, j = search_best_node(children_list, parent_n)
        node_path.append(children)
        node_path.append(j)

    return node_tree, node_path
