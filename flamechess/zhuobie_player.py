from .zhuobie import *
from .MCTS import *
from .socketIO import *
import time


class Wrapped(Client):
    def __init__(self, userId):
        super(Wrapped, self).__init__(1002, userId)
        self.game = Game()
        self.tree = None
        self.first_run = True
        time.sleep(0.5)
        self.set_data('000000ZZZ0000000zzz000000')

    def on_update(self, chesspos):
        if chesspos == self.chesspos or self.first_run and chesspos == '000000ZZZ0000000zzz000000':
            return
        # print("\n".join([chesspos[i:i+5] for i in range(0, 25, 5)]))
        state = []
        change = {'z': 1, 'Z': -1, '0': 0}
        for line in [chesspos[6:9], chesspos[11:14], chesspos[16:19]]:
            new_line = []
            for spot in line:
                new_line.append(change[spot])
            state.append(new_line)
        if self.first_run:
            self.tree = Tree(state, self.game, -1, max_node=500)
            self.first_run = False
        else:
            # print([child.action for child in self.tree.root.children])
            # tmp.append(self.tree.root)
            self.tree.update_by_state(state)
        best_child = self.tree.search()
        new_state = best_child.state
        turn = best_child.turn
        new_chesspos = '00000'
        new_change = {1: 'z', -1: 'Z', 0: '0'}
        for line in new_state:
            new_chesspos += '0'
            for spot in line:
                new_chesspos += new_change[spot]
            new_chesspos += '0'
        new_chesspos += '00000'
        self.chesspos = new_chesspos
        self.set_data(new_chesspos)
        time.sleep(0.5)
        if self.tree.root.game.end_game(new_state, turn):
            self.disconnect()


def main(userId):
    Wrapped(userId)
