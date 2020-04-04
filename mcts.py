from search import search, select_best_action
from _mcts import Node, NODE_TREE_DICT
from backprop import backprop, join_trees
from tictoctoe import TicTocToe
import copy
import numpy as np

MCTS_STEPS = 2

game = TicTocToe()
done = False
while not done:
    game.render()
    print("It's your turn, " + game.turn + ". Move to which place?")
    print('empty moves: ', game.empty_moves())
    move = input()
    done = game.step(move)
    game.render()
    if done and not (done == 'tie'):
        break
    elif done:
        print("\nGame Over.\n")
        print("****  Tie!  ****")
        break
    print('Agent is thinking ...')
    # find out the move of MCTS
    tree_lenght = []
    copy_of_NODE_TREE_DICT = copy.deepcopy(NODE_TREE_DICT)
    unexplored_actions = game.empty_moves()
    if len(unexplored_actions) > 1:
        copy_of_NODE_TREE_DICT['unexplored_actions'] = unexplored_actions
        for i in range(MCTS_STEPS):
            node_tree, node_path = search(copy_of_NODE_TREE_DICT)
            if len(node_tree['unexplored_actions']) == 1:
                # update the scores of 'n' and total score bcz of changes in 'n' when selecting node
                copy_of_NODE_TREE_DICT = join_trees(copy_of_NODE_TREE_DICT, node_path, node_tree)
                backprop(copy_of_NODE_TREE_DICT, node_path)
                continue
            # mcts
            node = Node(node_tree=node_tree, game=game, node_path=node_path)
            node.expand()
            # update the scores
            copy_of_NODE_TREE_DICT = join_trees(copy_of_NODE_TREE_DICT, node_path, node_tree)
            backprop(copy_of_NODE_TREE_DICT, node_path)
            node_path = [] if not node_path else node_path
            tree_lenght.append(len(node_path) // 2)
        # select best action from copy_of_NODE_TREE_DICT and execute it!
        action = select_best_action(copy_of_NODE_TREE_DICT)
        print('tree grain -', np.mean(tree_lenght))

    else:  # one possible action left then execute it!
        action = unexplored_actions[0]

    action = select_best_action(copy_of_NODE_TREE_DICT)
    done = game.step(action)
    if done and not (done == 'tie'):
        game.render()
        break
    elif done:
        game.render()
        print("\nGame Over.\n")
        print("****  Tie!  ****")
        break
