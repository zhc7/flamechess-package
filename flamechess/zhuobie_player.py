from .zhuobie import *
from .MCTS import *
from .socketIO import *


class Wrapped(Client):
    def __init__(self, userId):
        super(Wrapped, self).__init__(1002, userId)
        self.game = Game()
        self.tree = None
        self.first_run = True

    def on_update(self, chesspos):
        if self.first_run:
            self.tree = Tree(chesspos, self.game, -1, 300)
            self.first_run = False
        else:
            self.tree.update_by_state(chesspos)
        new_state = self.tree.search().state
        self.set_data(new_state)


def main(userId):
    Wrapped(userId)
