class Game:
    def __init__(self):
        self.available = {
            (0, 0): [(1, 0), (0, 1)],
            (0, 1): [(0, 0), (0, 2), (1, 0), (1, 2)],
            (0, 2): [(0, 1), (1, 2)],
            (1, 0): [(0, 0), (2, 0)],
            (1, 2): [(0, 2), (2, 2)],
            (2, 0): [(1, 0), (2, 1)],
            (2, 1): [(1, 0), (2, 0), (1, 2), (2, 2)],
            (2, 2): [(2, 1), (1, 2)],
        }
        self.corners = {
            ((0, 1), (1, 0)): (0, 0),
            ((1, 2), (2, 1)): (2, 2),
            ((2, 1), (1, 0)): (2, 0),
            ((1, 0), (1, 2)): (0, 2)
        }
        self.initial_state = [
            [-1, -1, -1],
            [0, 0, 0],
            [1, 1, 1]
        ]

    def available_actions(self, state, player):
        available = []
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

    def next_state(self, state, action, player):
        (y1, x1), (y2, x2) = action
        state = list(state)
        state[y1][x1] = 0
        state[y2][x2] = player
        for side1, side2 in self.corners.keys():
            corner = self.corners[(side1, side2)]
            if side1 == side2 == player and corner != player:
                x, y = corner
                state[y][x] = 0
        return state

    @staticmethod
    def end_game(state):
        flatten = sum(state, [])
        if flatten.count(1) <= 1:
            return -1
        elif flatten.count(-1) <= 1:
            return 1
        else:
            return 0
