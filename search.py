import numpy as np
import copy
from helpers import set_value_by_path

C = 0.2  # exploration factor constant, the higher it is the more exploration is done


def select_best_action(node_tree_dict):
    children_list = node_tree_dict['children']
    best_child = None
    best_score = np.float('-inf')
    for i, child in enumerate(children_list):
        child_score = child['total_score']
        # below I don't use upper confidence bound heuristic
        if child_score >= best_score:
            best_score = child_score
            best_child = child
    # return best action
    return best_child['node_name']


def select_node_for_expansion(children_list, parent_n):
    best_child = None
    best_score = np.float('-inf')
    j = None
    for i, child in enumerate(children_list):
        child_score = child['total_score']
        child_score += C * np.sqrt(2 * np.log(parent_n) / child['n'])  # upper confidence bound heuristic
        if child_score >= best_score:
            best_score = child_score
            best_child = child
            j = i

    return best_child, j


# def search(node_tree_dict):
#     node_tree = copy.deepcopy(node_tree_dict)
#     node_path = []
#     children = 'children'
#     counter = 0  # to check whether input node is root or not
#     j = -1
#     while True:
#         try:
#             parent_n = node_tree['n']
#             children_list = node_tree[children]
#             # if node does not have children then 'n' wont be increased!
#             j = [] if j == -1 else [j]
#             _ = set_value_by_path(node_tree_dict, node_path + j + ['n'],
#                                   (parent_n + 1))  # if a node passed take into account that
#         except KeyError:
#             node_path = None if counter == 0 else node_path
#             return node_tree, node_path  # if key error return current node
#         node_tree, j = select_node_for_expansion(children_list, parent_n)
#         node_path.append(children)
#         node_path.append(j)
#         counter += 1
#
#     return node_tree, node_path


def search(node_tree_dict):
    node_tree = copy.deepcopy(node_tree_dict)
    node_path = []
    children = 'children'
    counter = 0  # to check whether input node is root or not
    j = -1
    while True:
        parent_n = node_tree['n']
        if children in node_tree.keys():
            children_list = node_tree[children]
            # if node does not have children then 'n' wont be increased!
            j = [] if j == -1 else [j]
            _ = set_value_by_path(node_tree_dict, node_path + j + ['n'],
                                  (parent_n + 1))  # if a node passed take into account that
        else:
            node_path = None if counter == 0 else node_path
            return node_tree, node_path  # if key error return current node
        node_tree, j = select_node_for_expansion(children_list, parent_n)
        node_path.append(children)
        node_path.append(j)
        counter += 1

    return node_tree, node_path
