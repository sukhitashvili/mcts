from abc import ABCMeta, abstractmethod, ABC
import random
from tictoctoe import TicTocToe
from _collections import OrderedDict

NODE_TREE_DICT = dict()  # node_tree_dict -> {'node_name': 'node_1', 'children': [{}, {}, ...], 'score': float, 'n': int, 'unexplored_actions': [action_1, action_2, ...]}
NODE_TREE_DICT['node_name'] = 'root_node'
# NODE_TREE_DICT['children'] = []
NODE_TREE_DICT['node_score'] = 0
NODE_TREE_DICT['total_score'] = 0
NODE_TREE_DICT['n'] = 0
NODE_TREE_DICT['unexplored_actions'] = []
NODE_TREE_DICT['board'] = OrderedDict()


class MCTS(metaclass=ABCMeta):
    def __init__(self):
        pass

    # @abstractmethod
    # def update(self):
    #     """
    #     updates the scores from bottom up to the root tree.
    #     :return:
    #     """
    #     raise NotImplementedError

    @abstractmethod
    def simulate(self, first_action, possible_actions: list, repeat: int = 1):
        raise NotImplementedError

    # @abstractmethod
    # def select(self):
    #     """
    #     selects node dependent on children node's scores of working_node and set best one at working_node.
    #     :return:
    #     """
    #     raise NotImplementedError

    @abstractmethod
    def expand(self):
        raise NotImplementedError


class Node(MCTS, ABC):
    def __init__(self, node_path: list, node_tree: dict, game: TicTocToe):
        super().__init__()
        self.node_tree = node_tree
        self.game = game
        self.action_size = len(self.node_tree['unexplored_actions'])
        if not self.action_size > 1:  # if actions left, execute them and then simulate!
            raise RuntimeError('left actions must be more then 1')
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
                    won -= 1
                    return won
            elif done:  # if ended tie!
                won += 0
                return won

            # random simulation of play
            actions = possible_actions.copy()
            while not done:
                move, actions = self.default_polocy(actions)
                done = game.step(move, simulation=True)
                print(actions)
                print(done)
                game.render()
                if done and not (done == 'tie'):
                    winner = game.turn
                    if winner == self.game.turn:  # if the winner is the same whose turn is in real game!
                        won += 1
                        break
                    else:  # if first player loss!
                        won -= 1
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
            score = self.simulate(action, possible_actions, repeat=1)
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
