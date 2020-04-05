from abc import ABCMeta, abstractmethod, ABC
import random
from tictoctoe import TicTocToe
from _collections import OrderedDict
from helpers import get_value_by_path, set_value_by_path
import numpy as np
import copy

C = 0.2  # exploration factor constant, the higher it is the more exploration is done

NODE_TREE_DICT = dict()
NODE_TREE_DICT['node_name'] = 'root_node'
NODE_TREE_DICT['node_score'] = 0
NODE_TREE_DICT['total_score'] = 0
NODE_TREE_DICT['n'] = 0
NODE_TREE_DICT['unexplored_actions'] = []
NODE_TREE_DICT['board'] = OrderedDict()


class MCTS(metaclass=ABCMeta):
    def __init__(self):
        pass

    @staticmethod
    def backprop(node_tree_dict, node_path):
        """
        updates the scores from the node up to the root node.
        :param node_tree_dict: dict of node trees.
        :param node_path: path to the modified node.
        :return: None
        """
        if node_path:
            for _ in range(len(node_path) // 2):
                modified_node = get_value_by_path(node_tree_dict, node_path)
                children_list = modified_node['children']
                modified_node['total_score'] = (modified_node['node_score'] + np.sum(
                    [child['total_score'] for child in children_list])) / modified_node['n']
                node_path = node_path[:-2]
            # for the last time change root level value
            children_list = node_tree_dict['children']
            node_tree_dict['total_score'] = (node_tree_dict['node_score'] + np.sum(
                [child['total_score'] for child in children_list])) / node_tree_dict['n']

        else:
            children_list = node_tree_dict['children']
            node_tree_dict['total_score'] = (node_tree_dict['node_score'] + np.sum(
                [child['total_score'] for child in children_list])) / node_tree_dict['n']

    @staticmethod
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

    @staticmethod
    def select_node(node_tree_dict):
        """
        selects node for expansion from node tree.
        :param node_tree_dict: node tree dict
        :return: node dict and path to that node
        """
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
                parent_path = [] if j == -1 else node_path
                # if a node passed take into account that
                _ = set_value_by_path(node_tree_dict, parent_path + ['n'], (parent_n + 1))

            else:
                node_path = None if counter == 0 else node_path
                return node_tree, node_path  # if key error return current node
            node_tree, j = MCTS.select_node_for_expansion(children_list, parent_n)
            node_path.append(children)
            node_path.append(j)
            counter += 1

    @staticmethod
    def select_best_action(node_tree_dict):
        """
        select best action for agent move.
        :param node_tree_dict: node tree dict
        :return: best action.
        """
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

    @abstractmethod
    def simulate(self, first_action, possible_actions: list, repeat: int = 1):
        raise NotImplementedError

    @abstractmethod
    def expand(self):
        raise NotImplementedError


class Node(MCTS, ABC):
    def __init__(self, node_path: list, node_tree: dict, game: TicTocToe):
        super().__init__()
        self.node_tree = node_tree
        self.game = game
        self.action_size = len(self.node_tree['unexplored_actions'])
        if self.action_size == 0:  # if actions left, execute them and then simulate!
            print('node_tree', self.node_tree)
            raise RuntimeError('there are 0 action left!')
        # find out whose turn it is
        node_path_len = len(node_path) // 2 if node_path else 0
        if node_path_len % 2:  # when odd it's second player's turn
            self.simulation_turn = 'X' if self.game.turn == 'O' else 'O'
        else:
            self.simulation_turn = self.game.turn

    @staticmethod
    def remove(list_obj, item):
        l = list_obj.copy()
        l.remove(item)
        return l

    @staticmethod
    def join_trees(node_tree_dict, node_path, node_tree):
        if node_path:
            node_tree_dict = set_value_by_path(node_tree_dict, node_path,
                                               node_tree)  # replaces an old child node by new one with children!
            return node_tree_dict
        else:
            node_tree_dict = node_tree  # if root node then keep it
            return node_tree_dict

    @staticmethod
    def default_polocy(action_list):
        action = random.choice(action_list)
        action_list.remove(action)
        return action, action_list

    def simulate(self, first_action, possible_actions: list, repeat: int = 1):
        won = 0
        # now execute left actions!
        for i in range(repeat):
            # init the game
            game = TicTocToe(game_board=self.node_tree['board'].copy(), turn=self.simulation_turn,
                             count=(9 - self.action_size))
            done = game.step(first_action, simulation=True)
            if done and not (done == 'tie'):
                winner = game.turn
                if winner == self.game.turn:  # if the winner is the same whose turn is in real game!
                    won += 1
                    return won
                else:  # if first player loss!
                    won -= 2
                    return won
            elif done:  # if ended tie!
                won += 0
                return won

            # random simulation of play
            actions = possible_actions.copy()
            while not done:
                move, actions = self.default_polocy(actions)
                done = game.step(move, simulation=True)
                if done and not (done == 'tie'):
                    winner = game.turn
                    if winner == self.game.turn:  # if the winner is the same whose turn is in real game!
                        won += 1
                        break
                    else:  # if first player loss!
                        won -= 2
                        break

                elif done:  # if ended tie!
                    won += 0
                    break

        return won / repeat

    def expand(self):
        children = []
        for action in self.node_tree['unexplored_actions']:
            self.node_tree['n'] += 1
            possible_actions = self.remove(self.node_tree['unexplored_actions'], action)
            score = self.simulate(action, possible_actions, repeat=50)
            # create a new child node with stats
            child_board = self.node_tree['board'].copy()
            child_board[action] = self.simulation_turn
            child = {'node_score': score,
                     'total_score': score,  # when node does not have children its score the the total score!
                     'n': 1,
                     'unexplored_actions': possible_actions,
                     'board': child_board,
                     'node_name': action}
            children.append(child)
        self.node_tree['unexplored_actions'] = []  # after all actions has been explored in the node!
        self.node_tree['children'] = children


def mcts_step(game, node_tree_dict, step_number: int = 20):
    for i in range(step_number):
        node_tree, node_path = Node.select_node(node_tree_dict)
        # mcts
        if node_tree['unexplored_actions'] == []:
            node_tree['n'] += 1  # after some increases selection of the node will stop and exploration will continue
            continue
        node = Node(node_tree=node_tree, game=game, node_path=node_path)
        node.expand()
        # update the scores
        node_tree_dict = node.join_trees(node_tree_dict, node_path, node_tree)
        node.backprop(node_tree_dict, node_path)

    # select best action from copy_of_NODE_TREE_DICT and execute it!
    action = node.select_best_action(node_tree_dict)
    return action
