import math
import random
from .jiuqi import Game


class Node:
    def __init__(self, parent, state, game):
        self.count = 0
        self.black_win = 0
        self.white_win = 0
        self.win = 0
        self.children = []
        self.parent = parent
        self.turn = -parent.turn
        self.state = state
        self.game = game  # 规则
        self.all_actions = game.available_actions(state)
        self.tried_actions = []

    @staticmethod
    def UCB(win, count, t):
        Cts = math.sqrt(2 * math.log(t) / count)
        It = win / count + Cts
        return It

    def biggest_UCB(self):
        biggest = (0, None)
        for child in self.children:
            ucb = self.UCB(child.win, child.count, self.count)
            if ucb > biggest[0]:
                biggest = (ucb, child)
        return biggest[1]  # type: Node

    def expand(self):
        untried_actions = [action for action in self.all_actions if action not in self.tried_actions]
        action = random.choice(untried_actions)
        self.tried_actions.append(action)
        next_state = self.game.next_state(self.state, action)
        child = Node(self, next_state, self.game)
        self.children.append(child)
        return child

    def renew(self, reward):
        self.count += 1
        self.black_win += reward
        self.white_win += 1 - reward
        if self.parent.turn == 1:
            self.win = self.black_win
        else:
            self.win = self.white_win

    def forward(self):
        if set(self.tried_actions) != set(self.all_actions):  # 没有被完全展开
            child = self.expand()
            reward = child.simulate()
        else:
            child = self.biggest_UCB()  # 选择UCB最大的子节点
            reward = child.forward()
        self.renew(reward)
        return reward

    def simulate(self):
        state = self.state
        while not self.game.end_game(state):
            action = random.choice(self.game.available_actions(state))
            state = self.game.next_state(state, action)
        return self.game.end_game(state)


class RootNode(Node):
    def __init__(self, state, game):
        self.count = 0
        self.black_win = 0
        self.white_win = 0
        self.win = 0
        self.children = []
        self.turn = 1
        self.state = state
        self.game = game  # 规则
        self.all_actions = game.available_actions(state)
        self.tried_actions = []


class Tree:
    def __init__(self, initial_state, game):
        self.root = RootNode(initial_state, game)
        self.main()

    def main(self):
        ok = True
        while ok:
            self.root.forward()
