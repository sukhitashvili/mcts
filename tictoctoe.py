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
    def __init__(self, game_board=board, turn='X'):
        self.board = game_board
        self.turn = turn
        self.count = 0

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

    def empty_moves(self):
        moves = []
        for key in self.board.keys():
            if self.board[key] == ' ':
                moves.append(key)
        return moves

    def step(self, move):
        if self.board[move] == ' ':
            self.board[move] = self.turn
            self.count += 1
        else:
            print("That place is already filled.\nMove to which place?")

        # Now we will check if player X or O has won,for every move after 5 moves.
        if self.count >= 0:  # 5
            if self.board['7'] == self.board['8'] == self.board['9'] != ' ':  # across the top
                self.render()
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
                return True
            elif self.board['4'] == self.board['5'] == self.board['6'] != ' ':  # across the middle
                self.render()
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
                return True
            elif self.board['1'] == self.board['2'] == self.board['3'] != ' ':  # across the bottom
                self.render()
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
                return True
            elif self.board['1'] == self.board['4'] == self.board['7'] != ' ':  # down the left side
                self.render()
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
                return True
            elif self.board['2'] == self.board['5'] == self.board['8'] != ' ':  # down the middle
                self.render()
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
                return True
            elif self.board['3'] == self.board['6'] == self.board['9'] != ' ':  # down the right side
                self.render()
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
                return True
            elif self.board['7'] == self.board['5'] == self.board['3'] != ' ':  # diagonal
                self.render()
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
                return True
            elif self.board['1'] == self.board['5'] == self.board['9'] != ' ':  # diagonal
                self.render()
                print("\nGame Over.\n")
                print(" **** " + self.turn + " won. ****")
                return True
        # Now we have to change the player after every move.
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'


if __name__ == '__main__':
    TicTocToe().play()