from search import search, select_best_action
from _mcts import Node, NODE_TREE_DICT
from backprop import backprop, join_trees
from tictoctoe import TicTocToe
import copy

MCTS_STEPS = 100

game = TicTocToe()
done = False
while not done:
    game.render()
    print("It's your turn, " + game.turn + ". Move to which place?")
    print('empty moves: ', game.empty_moves())
    move = input()
    done = game.step(move)
    if done and not (done == 'tie'):
        game.render()
        break
    elif done:
        game.render()
        print("\nGame Over.\n")
        print("****  Tie!  ****")
        break

    # find out the move of MCTS
    copy_of_NODE_TREE_DICT = copy.deepcopy(NODE_TREE_DICT)
    for _ in range(MCTS_STEPS):
        node_tree, node_path = search(copy_of_NODE_TREE_DICT)
        node_tree['unexplored_actions'] = game.empty_moves()
        # mcts
        node = Node(node_tree=node_tree, game=game)
        node.expand()
        print('node tree ->', node_tree)
        exit()
        # update the scores
        join_trees(copy_of_NODE_TREE_DICT, node_path, node_tree)
        backprop(copy_of_NODE_TREE_DICT, node_path)

    # select best action from copy_of_NODE_TREE_DICT and execute it!
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
