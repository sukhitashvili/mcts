from search import search
from _mcts import Node, NODE_TREE_DICT
from tictoctoe import TicTocToe

game = TicTocToe()
done = False
while not done:
    game.render()
    print("It's your turn, " + game.turn + ". Move to which place?")
    print('empty moves: ', game.empty_moves())
    move = input()
    done = game.step(move)
    if done:
        break
    # find out the move of MCTS
    node = Node(node_tree=NODE_TREE_DICT, game=game)
    node_tree, node_path = search(NODE_TREE_DICT)

