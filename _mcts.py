from abc import ABCMeta, abstractmethod, ABC
import random
from tictoctoe import TicTocToe

NODE_TREE_DICT = dict()  # node_tree_dict -> {'node_name': 'node_1', 'children': [{}, {}, ...], 'score': float, 'n': int, 'unexplored_actions': [action_1, action_2, ...]}
NODE_TREE_DICT['node_name'] = 'node_1'
# NODE_TREE_DICT['children'] = []
NODE_TREE_DICT['node_score'] = 0
NODE_TREE_DICT['total_score'] = 0
NODE_TREE_DICT['n'] = 0
NODE_TREE_DICT['unexplored_actions'] = []


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
    def simulate(self, game, first_action, possible_actions: list, repeat: int = 1):
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
        """
        expands node tree or exploits left actions.
        :return: children nodes list that should be added to NODE_TREE_DICT into proper place.
        """
        raise NotImplementedError


class Node(MCTS, ABC):
    def __init__(self, node_tree: dict, game: TicTocToe):
        super().__init__()
        self.node_tree = node_tree
        self.game = game

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

    def simulate(self, game, first_action, possible_actions: list, repeat: int = 1):
        won = 0
        # firstly execute first action and see what happens!
        # here we do not need the 'repeat' loop, if game ends in one step
        # the same result will be performed every time, bcz our game is not stochastic.
        done = game.step(first_action, simulation=True)
        if done and not (done == 'tie'):
            winner = game.turn
            if winner == self.game.turn:  # if winner is the same whose turn was first!
                won += 1
                return won
            else:  # if first player loss!
                won -= 1
                return won
        elif done:  # if ended tie!
            won += 0
            return won

        # now execute left actions!
        for i in range(repeat):
            actions = possible_actions.copy()
            while not done:
                move, actions = self.default_polocy(actions)
                done = game.step(move, simulation=True)
                if done and not (done == 'tie'):
                    winner = game.turn
                    if winner == self.game.turn:  # if winner is the same whose turn was first!
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
        if len(self.node_tree['unexplored_actions']) != 0:  # if actions left, execute them and then simulate!
            children = []
            for action in self.node_tree['unexplored_actions']:
                self.node_tree['n'] += 1
                game = TicTocToe(game_board=self.game.board.copy(), turn=self.game.turn, count=self.game.count)
                possible_actions = self.remove(self.node_tree['unexplored_actions'], action)
                score = self.simulate(game, action, possible_actions, repeat=50)
                # create a new child node with stats
                child = {'node_score': score,
                         'total_score': score,  # when node does not have children its score the the total score!
                         'n': 1,
                         'unexplored_actions': possible_actions,
                         'node_name': action}
                children.append(child)
            self.node_tree['unexplored_actions'] = []  # after all actions has been explored in the node!
            self.node_tree['children'] = children
