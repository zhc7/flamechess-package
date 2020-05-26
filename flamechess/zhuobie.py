from copy import deepcopy


class Game:
    def __init__(self):
        self.available = {
            (0, 0): [(1, 0), (0, 1)],
            (0, 1): [(0, 0), (0, 2), (1, 0), (1, 2)],
            (0, 2): [(0, 1), (1, 2)],
            (1, 0): [(0, 0), (2, 0), (0, 1), (2, 1)],
            (1, 2): [(0, 2), (2, 2), (0, 1), (2, 1)],
            (2, 0): [(1, 0), (2, 1)],
            (2, 1): [(1, 0), (2, 0), (1, 2), (2, 2)],
            (2, 2): [(2, 1), (1, 2)],
        }
        self.corners = {
            ((0, 1), (1, 0)): (0, 0),
            ((1, 2), (2, 1)): (2, 2),
            ((2, 1), (1, 0)): (2, 0),
            ((0, 1), (1, 2)): (0, 2)
        }
        self.initial_state = [
            [-1, -1, -1],
            [0, 0, 0],
            [1, 1, 1]
        ]

    def available_actions(self, state, player):
        available = []
        state = deepcopy(state)
        for y, line in enumerate(state):
            for x, place in enumerate(line):
                if place != player:
                    continue
                avail = self.available[(y, x)]
                for p in avail:
                    yp, xp = p
                    if state[yp][xp] == 0:
                        available.append(((y, x), p))
        return available

    @staticmethod
    def get(state, place):
        return state[place[0]][place[1]]

    def next_state(self, state, action, player):
        (y1, x1), (y2, x2) = action
        state = deepcopy(state)
        state[y1][x1] = 0
        state[y2][x2] = player
        for side1, side2 in self.corners.keys():
            corner = self.corners[(side1, side2)]
            if self.get(state, side1) == self.get(state, side2) == player and self.get(state, corner) != player:
                y, x = corner
                state[y][x] = 0
        return state

    def end_game(self, state, turn):
        state = deepcopy(state)
        if not self.available_actions(state, turn):
            return -turn
        flatten = sum(state, [])
        if flatten.count(1) <= 1:
            return -1
        elif flatten.count(-1) <= 1:
            return 1
        else:
            return 0
