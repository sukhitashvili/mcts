import numpy as np
from helpers import set_value_by_path, get_value_by_path


def join_trees(node_tree_dict, node_path, node_tree):
    if node_path:
        node_tree_dict = set_value_by_path(node_tree_dict, node_path, node_tree)  # replaces an old child node by new one with children!
        return node_tree_dict
    else:
        node_tree_dict = node_tree  # if root node then keep it
        return node_tree_dict


def backprop(node_tree_dict, node_path):
    if node_path:
        for _ in range(len(node_path) // 2):
            modified_node = get_value_by_path(node_tree_dict, node_path)
            children_list = modified_node['children']
            modified_node['total_score'] = (modified_node['node_score'] + np.sum([child['total_score'] for child in children_list])) / modified_node['n']
            node_path = node_path[:-2]
        # for the last time (bcz root level value does not change)
        children_list = node_tree_dict['children']
        node_tree_dict['total_score'] = (node_tree_dict['node_score'] + np.sum([child['total_score'] for child in children_list])) / node_tree_dict['n']

    else:
        children_list = node_tree_dict['children']
        node_tree_dict['total_score'] = (node_tree_dict['node_score'] + np.sum([child['total_score'] for child in children_list])) / node_tree_dict['n']
