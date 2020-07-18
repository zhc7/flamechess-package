from jpype import *
from jpype.types import *
import jpype.imports


jarpath = ["../java/jars/*"]
startJVM(classpath=jarpath, convertStrings=False)


from com.jingbh.flamechess import State
from com.jingbh.flamechess import Coordinates
from com.jingbh.flamechess.jiuqi import Action
from com.jingbh.flamechess.jiuqi import Game as JGame


class Game:
    def __init__(self):
        self.initial_state = \
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.game = JGame

    def convert_state(self, state):
        return State(JArray(JByte, 2)(state))

    def convert_action(self, action):
        moves, eats = action
        cor_moves = []
        cor_eats = []
        for move in moves:
            cor_move = Coordinates(*move)
            cor_moves.append(cor_move)
        if eats:
            for eat in eats:
                cor_eat = Coordinates(*eat)
                cor_eats.append(cor_eat)
            new_eats = JArray(Coordinates, 1)(cor_eats)
        else:
            new_eats = None
        return Action(JArray(Coordinates, 1)(cor_moves), new_eats)

    def available_actions(self, state, player, flag):
        new_state = self.convert_state(state)
        return self.game.availableActions(new_state, JByte(player), JString(flag))

    def next_state(self, state, action, player, flag):
        new_state = self.convert_state(state)
        new_action = self.convert_action(action)
        return self.game.nextState(new_state, new_action, JByte(player), JString(flag))

    def end_game(self, state, turn, flag):
        new_state = self.convert_state(state)
        return self.game.endGame(new_state, JByte(turn), JString(flag))

    def evaluate(self, state, turn):
        new_state = self.convert_state(state)
        return self.game.evaluate(new_state, JByte(turn))


if __name__ == '__main__':
    game = Game()
    test = game.next_state(game.initial_state, (((1, 2),), None), 1, "layout")
    print(test)


