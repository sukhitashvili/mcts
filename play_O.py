from mcts import NODE_TREE_DICT, mcts_step
from tictoctoe import TicTocToe
import copy


MCTS_STEPS = 20

game = TicTocToe()
done = False
while not done:

    print("Agent's turn ...")
    # find out the move of MCTS
    copy_of_NODE_TREE_DICT = copy.deepcopy(NODE_TREE_DICT)
    unexplored_actions = game.empty_moves()

    copy_of_NODE_TREE_DICT['unexplored_actions'] = unexplored_actions
    copy_of_NODE_TREE_DICT['board'] = game.board
    action = mcts_step(game, copy_of_NODE_TREE_DICT, MCTS_STEPS)

    done = game.step(action)
    game.render()
    if done and not (done == 'tie'):
        break
    elif done:
        print("\nGame Over.\n")
        print("****  Tie!  ****")
        break

    print("It's your turn, " + game.turn + ". Move to which place?")
    move = input()
    done = game.step(move)
    game.render()
    if done and not (done == 'tie'):
        break
    elif done:
        print("\nGame Over.\n")
        print("****  Tie!  ****")
        break
