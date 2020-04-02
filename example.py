

my_iter = 0


class Re:
    def __init__(self):
        super().__init__()
        global my_iter

        my_iter += 1
        self._print(my_iter)
        self.recursion()

    def _print(self, i):
        print(i)

    def recursion(self):
        if my_iter >= 50:
            print('stoped at ', my_iter)
            return
        else:
            Re()


if __name__ == '__main__':
    r = Re()
