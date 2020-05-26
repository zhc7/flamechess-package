# 还未完成！！！ UNCOMPLETED！！！
class Game:
    def __init__(self):
        self.lines = [
            [(1, 1), (2, 1), (3, 1)],
            [(1, 3), (2, 3), (3, 3)],
            [(0, 4), (2, 4), (4, 4)],
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
            [(1, 1), (2, 2), (3, 3), (4, 4)],
            [(3, 1), (2, 2), (1, 3), (0, 4)],
            [(2, 0), (1, 1)],
            [(2, 0), (3, 1)],
        ]

    @staticmethod
    def get_place(state, place):
        return state[place[1]][place[0]]

    def available_actions(self, state, player):
        available = []
        for line in self.lines:
            for index, place in enumerate(line):
                if self.get_place(state, place) == player:
                    left = max(index - 1, 0)
                    right = min(index + 1, len(line))
                    left_place = self.get_place(state, line[left])
                    right_place = self.get_place(state, line[right])
                    if not left_place:
                        available.append(line[left])
                    elif player == 1:
                        pass
                    if not right_place:
                        available.append(line[right])
