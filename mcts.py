from abc import abstractmethod


class MCTS:
    def __init__(self):
        self.node_counet = 0  # counts the nodes on the tree
        self.node_tree = []  # list that should contain all the nodes

    @abstractmethod
    def update(self):
        """
        updates the scores from bottom up to the root tree.
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def simulate(self):
        """
        simulates game by randomly chosen action
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def select(self):
        """
        selects node dependent on children node's scores of working_node and set best one at working_node.
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def expand(self, node_class):
        """
        expands node tree or exploits left actions.
        :param node_class: child class of MCTS
        :return: None.
        """
        raise NotImplementedError
