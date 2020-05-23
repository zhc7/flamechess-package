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
        state = []
        change = {'Z': 1, 'z': -1, '0': 0}
        for line in [chesspos[6:9], chesspos[11:14], chesspos[16:19]]:
            new_line = []
            for spot in line:
                new_line.append(change[spot])
            state.append(new_line)
        if self.first_run:
            self.tree = Tree(state, self.game, -1, 300)
            self.first_run = False
        else:
            self.tree.update_by_state(state)
        new_state = self.tree.search().state
        new_chesspos = '00000'
        new_change = {1:'Z',-1:'z',0:'0'}
        for line in new_state:
            new_chesspos += '0'
            for spot in line:
                new_chesspos += new_change[spot]
            new_chesspos += '0'
        new_chesspos += '00000'
        self.set_data(new_chesspos)


def main(userId):
    Wrapped(userId)
