import math
import random
from copy import deepcopy


class Node:
    def __init__(self, parent, state, action, game, layer):
        self.count = 0
        self.black_win = 0
        self.white_win = 0
        self.win = 0
        self.children = []
        self.parent = parent
        self.turn = -parent.turn
        self.state = deepcopy(state)
        self.action = action
        self.game = game  # 规则
        self.layer = layer
        self.all_actions = game.available_actions(state, self.turn)
        self.tried_actions = []
        self.must_win = False

    def __del__(self):
        for child in self.children:
            del child

    @staticmethod
    def UCB(win, count, t, alpha=1):
        Cts = math.sqrt(2 * math.log(t) / count)
        It = win / count + alpha * Cts
        return It

    def best_child(self, alpha=1):
        biggest = (0, None)
        for child in self.children:
            if alpha == 0 and child.must_win:
                return child
            ucb = child.UCB(child.win, child.count, self.count, alpha)
            if ucb > biggest[0]:
                biggest = (ucb, child)
        return biggest[1]  # type: Node

    def expand(self):
        untried_actions = [action for action in self.all_actions if action not in self.tried_actions]
        action = random.choice(untried_actions)
        self.tried_actions.append(action)
        next_state = self.game.next_state(deepcopy(self.state), action, self.turn)
        child = Node(self, next_state, action, self.game, self.layer + 1)
        self.children.append(child)
        return child

    def renew(self, reward):
        self.count += 1
        self.black_win += max(reward, 0)  # 黑色赢的话reward为1
        self.white_win += max(-reward, 0)  # 白色赢的话reward为-1
        if self.turn == -1:  # 父节点是轮到黑棋下
            self.win = self.black_win
        else:
            self.win = self.white_win

    def forward(self, max_depth):
        if type(max_depth) == int and self.layer >= max_depth:  # 超过最大深度不再搜索
            return 'max_depth'
        end = self.game.end_game(self.state, self.turn)
        if end:  # 终局情况
            reward = end
            self.must_win = True
        elif set(self.tried_actions) != set(self.all_actions):  # 没有被完全展开
            child = self.expand()
            reward = child.simulate()
        else:  # 完全展开，选择子节点
            child = self.best_child()  # 选择UCB最大的子节点
            reward = child.forward(max_depth)
        if reward == 'max_depth':
            return reward
        else:
            self.renew(reward)
            return reward

    def simulate(self):
        state = deepcopy(self.state)
        turn = self.turn
        while not self.game.end_game(state, turn):
            try:
                action = random.choice(self.game.available_actions(state, turn))
            except IndexError:
                print(state, action)
            state = self.game.next_state(deepcopy(state), action, turn)
            turn = -turn
        reward = self.game.end_game(state, turn)
        self.renew(reward)
        return reward  # -1 or 1

    def count_node(self):
        num = 1
        for child in self.children:
            num += child.count_node()
        return num


class RootNode(Node):
    def __init__(self, state, game, player):
        self.count = 0
        self.black_win = 0
        self.white_win = 0
        self.win = 0
        self.children = []
        self.turn = player
        self.state = deepcopy(state)
        self.game = game  # 规则
        self.layer = 0
        self.all_actions = game.available_actions(state, self.turn)
        self.tried_actions = []


class Tree:
    def __init__(self, initial_state, game, initial_player, max_node, max_search_depth="unlimited"):
        self.root = RootNode(initial_state, game, initial_player)
        self.max_depth = max_search_depth
        self.max_node = max_node

    def search(self):
        ok = True
        while ok:
            response = self.root.forward(self.max_depth)
            if response == 'max_depth':
                ok = False
            if self.root.count_node() > self.max_node:
                ok = False
            if self.root.count > self.max_node:
                ok = False
        best_child = self.root.best_child(alpha=0)
        for child in self.root.children:
            if child != best_child:
                del child
        self.root = best_child
        if type(self.max_depth) == int:
            self.max_depth += 1
        return best_child

    def update(self, action):
        for child in self.root.children:
            if child.action != action:
                del child
            else:
                best_child = child
        self.root = best_child
        if type(self.max_depth) == int:
            self.max_depth += 1

    def update_by_state(self, state):
        for child in self.root.children:
            if child.state != state:
                del child
            else:
                best_child = child
        self.root = best_child
        if type(self.max_depth) == int:
            self.max_depth += 1


def beautiful_print(state):
    qi = {0: ' ', 1: 'O', -1: 'X'}
    for line in state:
        for spot in line:
            print(qi[spot], end=' ')
        print(end='\n')


def test(game, output=False):
    player1 = Tree(game.initial_state, game, 1, max_node=500)
    action = player1.search().action
    state = game.next_state(game.initial_state, action, 1)
    player2 = Tree(state, game, -1, max_node=500)
    while True:
        action = player2.search().action
        if output:
            beautiful_print(player2.root.state)
            print(player2.root.count, player2.root.win)
            input()
        if game.end_game(player2.root.state, -1):
            return game.end_game(player2.root.state, -1)
        player1.update(action)
        #
        action = player1.search().action
        if output:
            beautiful_print(player1.root.state)
            print(player1.root.count, player1.root.win)
            input()
        if game.end_game(player1.root.state, 1):
            return game.end_game(player1.root.state, 1)
        player2.update(action)
