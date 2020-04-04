from _collections import OrderedDict

board = OrderedDict()
board['9'] = ' '
board['8'] = ' '
board['7'] = ' '
board['6'] = ' '
board['5'] = ' '
board['4'] = ' '
board['3'] = ' '
board['2'] = ' '
board['1'] = ' '


class TicTocToe:
    def __init__(self, game_board=board, turn='X', count: int = 0):
        self.board = game_board
        self.turn = turn
        self.count = count

    def render(self):
        print(self.board['7'] + '|' + self.board['8'] + '|' + self.board['9'])
        print('-+-+-')
        print(self.board['4'] + '|' + self.board['5'] + '|' + self.board['6'])
        print('-+-+-')
        print(self.board['1'] + '|' + self.board['2'] + '|' + self.board['3'])

    def play(self):
        done = False
        while not done:
            self.render()
            print("It's your turn, " + self.turn + ". Move to which place?")
            print('empty moves: ', self.empty_moves())
            move = input()
            done = self.step(move)
            if done and not (done == 'tie'):
                self.render()
            elif done:
                self.render()
                print("\nGame Over.\n")
                print("****  Tie!  ****")

    def empty_moves(self):
        moves = []
        for key in self.board.keys():
            if self.board[key] == ' ':
                moves.append(key)
        return moves

    def step(self, move, simulation=False):
        if self.board[move] == ' ':
            self.board[move] = self.turn
            self.count += 1
        else:
            print("That place is already filled.\nMove to which place?")

        if self.board['7'] == self.board['8'] == self.board['9'] != ' ':  # across the top
            if not simulation:
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
            return True
        elif self.board['4'] == self.board['5'] == self.board['6'] != ' ':  # across the middle
            if not simulation:
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
            return True
        elif self.board['1'] == self.board['2'] == self.board['3'] != ' ':  # across the bottom
            if not simulation:
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
            return True
        elif self.board['1'] == self.board['4'] == self.board['7'] != ' ':  # down the left side
            if not simulation:
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
            return True
        elif self.board['2'] == self.board['5'] == self.board['8'] != ' ':  # down the middle
            if not simulation:
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
            return True
        elif self.board['3'] == self.board['6'] == self.board['9'] != ' ':  # down the right side
            if not simulation:
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
            return True
        elif self.board['7'] == self.board['5'] == self.board['3'] != ' ':  # diagonal
            if not simulation:
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
            return True
        elif self.board['1'] == self.board['5'] == self.board['9'] != ' ':  # diagonal
            if not simulation:
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
            return True

        # check if all states are filled
        if self.count >= 9:
            return 'tie'

        # Now we have to change the player after every move.
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'

        return False  # return False if not done!


if __name__ == '__main__':
    TicTocToe().play()
