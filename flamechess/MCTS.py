import math
import random
from .jiuqi import Game


class Node:
    def __init__(self, parent, state, action, game, layer):
        state = list(state)
        self.count = 0
        self.black_win = 0
        self.white_win = 0
        self.win = 0
        self.children = []
        self.parent = parent
        self.turn = -parent.turn
        self.state = list(state)
        self.action = action
        self.game = game  # 规则
        self.layer = layer
        self.all_actions = game.available_actions(state, self.turn)
        self.tried_actions = []

    def __del__(self):
        for child in self.children:
            del child

    @staticmethod
    def UCB(win, count, t):
        Cts = math.sqrt(2 * math.log(t) / count)
        It = win / count + Cts
        return It

    def best_child(self):
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
        next_state = self.game.next_state(self.state, action, self.turn)
        child = Node(self, next_state, action, self.game, self.layer + 1)
        self.children.append(child)
        return child

    def renew(self, reward):
        self.count += 1
        self.black_win += max(reward, 0)    # 黑色赢的话reward为1
        self.white_win += max(-reward, 0)   # 白色赢的话reward为-1
        if self.parent.turn == 1:
            self.win = self.black_win
        else:
            self.win = self.white_win

    def forward(self, max_depth):
        if self.layer >= max_depth:
            return 'max_depth'
        if set(self.tried_actions) != set(self.all_actions):  # 没有被完全展开
            child = self.expand()
            reward = child.simulate()
        else:
            child = self.best_child()  # 选择UCB最大的子节点
            reward = child.forward(max_depth)
        if reward == 'max_depth':
            return reward
        else:
            self.renew(reward)
            return reward

    def simulate(self):
        state = list(self.state)
        turn = self.turn
        while not self.game.end_game(state):
            action = random.choice(self.game.available_actions(state, turn))
            state = self.game.next_state(state, action, turn)
            turn = -turn
        return self.game.end_game(state)  # -1 or 1


class RootNode(Node):
    def __init__(self, state, game, player):
        self.count = 0
        self.black_win = 0
        self.white_win = 0
        self.win = 0
        self.children = []
        self.turn = player
        self.state = list(state)
        self.game = game  # 规则
        self.layer = 0
        self.all_actions = game.available_actions(state, self.turn)
        self.tried_actions = []


class Tree:
    def __init__(self, initial_state, max_search_depth, game, initial_player):
        self.root = RootNode(initial_state, game, initial_player)
        self.max_depth = max_search_depth

    def search(self):
        ok = True
        while ok:
            response = self.root.forward(self.max_depth)
            if response == 'max_depth':
                ok = False
        best_child = self.root.best_child()
        for child in self.root.children:
            if child != best_child:
                del child
        self.root = best_child
        self.max_depth += 1
        return best_child.action

    def update(self, action):
        for child in self.root.children:
            if child.action != action:
                del child
            else:
                best_child = child
        self.root = best_child
        self.max_depth += 1



