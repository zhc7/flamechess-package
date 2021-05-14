import itertools
from copy import deepcopy
import cProfile

class Game(object):
    def __init__(self):
        self.initial_state = \
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def available_actions(self, state, player, flag):
        """根据当前棋盘，对弈阶段和所执棋子返回可以下的坐标 
        return type:list example:[[步骤列表，提子列表]*n](play)  [[落子坐标/None,提子坐标/None]*n](layout)
        state:棋盘状态 
        flag:对弈阶段('layout':布局,'play':行棋)
        player:所执棋子 -1 or 1
        """

        me = player

        def jump_action(start, state, me):
            '''使用递归，dfs搜索，输入起始点坐标，就地修改函数外的actions变量'''
            jump_points = self.points_can_jump(state, start, me)
            if jump_points:
                for point in jump_points:
                    if actions:
                        for action in actions:
                            if action[-1] == start:
                                actions.append(action[0:-1] + (start, point))  # 将单一行棋合并到以初始起点为起点的行棋中
                    else:  # start为初始起点时
                        actions.append((start, point))
                    state = self.adjust_chessboard((start, point), state, me)  # 编辑棋盘时复制一个新棋盘，不会瞎改原棋盘
                    jump_action(point, state, me)
                    state[point[0]][point[1]] = 0
                    state[start[0]][start[1]] = me
                    remove_x=int((start[0]+point[0])/2)
                    remove_y=int((start[1]+point[1])/2)
                    state[remove_x][remove_y] = -me


        if flag == 'layout':  # 布棋阶段
            ret = []
            blank_indexes = []  # 空白点坐标
            for index, status in enumerate(sum(state, [])):
                if status == 0:
                    row = index // 14
                    col = index - row * 14
                    blank_indexes.append((row, col))
            if len(blank_indexes) == 196:  # 如果所有都是空白，那么第一步必须下棋盘中央方格的对角线两端
                ret.append(((6,6),None))
                ret.append(((7,7),None))
            elif len(blank_indexes) == 195:  #如果有一个不是空白，说明对手已经下在了(6,7)或(7,6)上，此时必须下在对角线另一侧
                if state[6][6] == 0:
                    ret.append(((6,6),None))
                elif state[7][7] == 0:
                    ret.append(((7,7),None))
            elif len(blank_indexes) == 0 or \
                (len(blank_indexes) == 1 and (not(state[6][6] and state[7][7]))):  # 如果所有格子都已经满了或刚被提一个，那么说明该进入提子阶段了
                if state[6][6] == -me:
                    ret.append((None,(6,6)))
                elif state[7][7] == -me:
                    ret.append((None,(7,7)))
            else:
                for b in blank_indexes:
                    ret.append((b, None))
            return ret
            # flag为layout时
        elif flag == 'play':
            mine = []
            enemies=[]
            blanks = []
            for index, status in enumerate(sum(state, [])):
                if status == me:
                    row = index // 14
                    col = index - row * 14
                    mine.append((row, col))
                elif status == -me:
                    row = index // 14
                    col = index - row * 14
                    enemies.append((row, col))
                elif status == 0:
                    row = index // 14
                    col = index - row * 14
                    blanks.append((row, col))
            all_actions = []
            for one in mine:
                actions = []
                actions_first_processed = []  # 第一次处理（不包括褡裢）
                actions_last = []  # 最后版本（考虑褡裢）
                jump_action(one, state, me)  # 就地修改actions,加入所有跳棋步骤（不包括所有提子）
                for a in actions:
                    if len(mine)>14 and 3 < len(enemies) <= 14:
                        if len(a) >=3:
                            actions_first_processed.append(self.action_process(a))  # 将跳提子加入跳棋步骤
                    else:
                        actions_first_processed.append(self.action_process(a))
                walks = self.go_around(one, state)  # 四周走棋
                for walk in walks:
                    actions_first_processed.append(walk)  # 四周走棋无需进行跳棋步骤的第一遍处理
                for a in actions_first_processed:
                    actions = self.find_dalian(state, a, me)  # 寻褡裢，返回包含了所有可能褡裢提子的步骤列表
                    for action in actions:
                        actions_last.append(action)
                for action in actions_last:
                    action = tuple(action)
                    all_actions.append(action)
            if len(mine) <= 14:
                went = []
                for a in all_actions:
                    for w in a[0][1:]:
                        went.append(w)
                went = set(went)
                blanks = set(blanks)
                available = list(blanks - went)  # 求差集
                products = list(itertools.product(mine, available))  # 组合
                for product in products:
                    product = [product, []]  # 补提子的位
                    actions = self.find_dalian(state, product, me)  # 找褡裢
                    for action in actions:
                        action = tuple(action)
                        all_actions.append(action)
            return all_actions

    def go_around(self, start, state):
        """往四周行棋，接收初始坐标，返回所有行棋步骤，包括提子补位"""
        actions = []
        row = start[0]
        col = start[1]
        possibilities = ((row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col))
        for possibility in possibilities:
            try:
                if 13 >= possibility[0] >= 0 == state[possibility[0]][possibility[1]] and 0 <= possibility[1] <= 13:
                    actions.append([(start, possibility), []])  # 包含补位
            except IndexError:
                pass
        return actions

    def adjust_chessboard(self, action, state, me):
        '''根据单步跳棋调整棋盘，返回新棋盘'''
        start = action[0]
        end = action[1]
        remove = (int((start[0] + end[0]) / 2), int((start[1] + end[1]) / 2))
        state[start[0]][start[1]] = 0
        state[end[0]][end[1]] = me
        state[remove[0]][remove[1]] = 0
        return state

    def action_process(self, action):
        """将只包含跳棋路线的步骤变为包含必提子的步骤"""
        removed = []
        for i in range(len(action) - 1):
            start = action[i]
            end = action[i + 1]
            remove = (int((start[0] + end[0]) / 2), int((start[1] + end[1]) / 2))
            removed.append(remove)
        return [action, removed]

    def find_dalian(self, state, action, me):
        """找寻褡裢，接收行棋步骤（包括行棋中提子），返回新的行棋步骤列表（包括可以提的子）"""
        new_actions = []  # 返回的行棋步骤列表
        n = 0  # 形成褡裢数
        remove = action[1]  # 这里即便不是跳棋，没有提子也必须补位
        start = action[0][0]
        end = action[0][-1]
        state[start[0]][start[1]] = 0
        state[end[0]][end[1]] = me
        row,col=end[0],end[1]
        for r in remove:
            state[r[0]][r[1]] = 0
        blocks = (((row, col), (row + 1, col), (row + 1, col + 1), (row, col + 1)),
                  ((row, col), (row + 1, col), (row + 1, col - 1), (row, col - 1)),
                  ((row, col), (row - 1, col), (row - 1, col - 1), (row, col - 1)),
                  ((row, col), (row - 1, col), (row - 1, col + 1), (row, col + 1)))
        for block in blocks:
            try:
                judge = True
                for index in block:
                    r, c = index[0], index[1]
                    if state[r][c] == 0 or state[r][c] != me or r<0 or c<0:
                        judge = False
                if judge:
                    n += 1
            except:  # 解决四个块中可能有坐标越界问题
                pass
        enemies = []  # 敌方棋子坐标（可提）
        for index, status in enumerate(sum(state, [])):
            if status == -me:
                row = index // 14
                col = index - row * 14
                enemies.append((row, col))
        combinations = list(itertools.combinations(enemies, n))  # 排列组合
        if combinations:
            if combinations[0]:
                action[1]=tuple(action[1])
                action=tuple(action)
                for removes in combinations:
                    route=action[0]
                    kill=list(action[1])
                    for r in removes:
                        kill.append(r)
                    new_actions.append((route,tuple(kill)))
                state[start[0]][start[1]] = me
                state[end[0]][end[1]] = 0
                for r in remove:
                    state[r[0]][r[1]] = -me
                return new_actions
        action[1] = tuple(action[1])
        state[start[0]][start[1]] = me
        state[end[0]][end[1]] = 0
        for r in remove:
            state[r[0]][r[1]] = -me
        return [action]  # 若无褡裢，为了返回值的统一性，再外包一层列表

    def points_can_jump(self, state, index, me):
        '''输入棋子的坐标，返回元组形式的可跳的点的坐标'''
        row, col = index[0], index[1]
        judge = ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
        possible = ((row - 2, col), (row + 2, col), (row, col - 2), (row, col + 2))
        can_jump = []
        for judge, possible in zip(judge, possible):
            if 0 <= possible[0] <= 13 and 0 <= possible[1] <= 13:
                row_j, col_j = judge[0], judge[1]
                row_p, col_p = possible[0], possible[1]
                if state[row_j][col_j] != 0 and state[row_j][col_j] != me and state[row_p][col_p] == 0:
                    can_jump.append((row_p, col_p))
        return can_jump

    def next_state(self, state, action, player, flag):
        """传入当前棋局，行棋步骤，行棋阶段和所持棋子，返回下一个棋局
        action example: [[(0, 0), (0, 2)], [(0, 1)]](play)  [(0,0),None](layout)"""
        me = player
        state1 = deepcopy(state)
        if flag == 'play':
            (x1, y1) = action[0][0]
            (x2, y2) = action[0][-1]
            killed = action[1]
            state1[x1][y1] = 0
            state1[x2][y2] = me
            for i in killed:
                (x, y) = i
                state1[x][y] = 0
        else:
            if action[0] is None:
                (x, y) = action[1]
                state1[x][y] = 0
            else:
                (x, y) = action[0]
                state1[x][y] = me
        return state1

    def end_game(self, state, turn, flag):
        """输入当前棋盘，返回谁赢谁输或和棋或未知
        若胜负已定则回复棋子代号：1/-1, 若平局则回0.5, 若胜负未定则回0"""
        if flag == "layout":
            return 0
        if not self.available_actions(state, turn, 'play'):
            return -turn
        chess_me = []
        chess_enemy = []
        for index, status in enumerate(sum(state, [])):
            if status == turn:
                row = index // 14
                col = index - row * 14
                chess_me.append((row, col))
            elif status == -turn:
                row = index // 14
                col = index - row * 14
                chess_enemy.append((row, col))
        if chess_me and (not chess_enemy):
            return turn
        if len(chess_me) <= 3:
            actions = self.available_actions(state, turn, 'play')
            maximum_kill = 0
            for action in actions:
                if len(action[1]) > maximum_kill:
                    maximum_kill = len(action[1])
            if maximum_kill < len(chess_enemy) <= 3:
                return 0.5
        return 0

    def evaluate(self, state, turn):
        '''评估胜率，返回一个0到1之间的数'''
        me_score = 0
        enemy_score = 0
        len_mine = 0
        len_not_mine = 0
        for status in sum(state, []):
            if status == turn:
                len_mine += 1
            elif status == -turn:
                len_not_mine += 1
        me_processed = set()
        enemy_processed = set()
        for x in range(0, 13):
            for y in range(0, 13):
                block = ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1))
                mine = []
                not_mine = []
                for dot in block:
                    if state[dot[0]][dot[1]] == turn:
                        mine.append(dot)
                    if state[dot[0]][dot[1]] == -turn:
                        not_mine.append(dot)
                if len(mine) == 3:
                    me_score += 3
                    for m in mine:
                        me_processed.add(m)
                elif len(mine) == 4:
                    me_score += 5
                    for m in mine:
                        me_processed.add(m)
                if len(not_mine) == 3:
                    enemy_score += 3
                    for m in not_mine:
                        enemy_processed.add(m)
                elif len(not_mine) == 4:
                    enemy_score += 5
                    for m in not_mine:
                        enemy_processed.add(m)
        me_score += (len_mine - len(me_processed))
        enemy_score += (len_not_mine - len(enemy_processed))
        try:
            ret = me_score / (me_score + enemy_score)
        except ZeroDivisionError:
            ret = 0.5
        return ret
    
    def evaluate_in_ending_part(self, state, turn):
        len_me = 0
        len_enemy = 0
        for status in sum(state, []):
            if status == turn:
                len_me += 1
            elif status == -turn:
                len_enemy += 1
        processed_me = set()
        processed_enemy = set()
        len_double_dalian_me=0
        len_triangle_me=0
        len_double_dalian_enemy=0
        len_triangle_enemy=0
        for x in range(12):
            for y in range(11):
                double_dalian_1 = ((x,y),(x,y+1),
                                    (x+1,y),(x+1,y+3),
                                    (x+2,y+2),(x+2,y+3))
                double_dalian_2 = ((x,y+2),(x,y+3),
                                    (x+1,y),(x+1,y+3),
                                    (x+2,y),(x+2,y+1))
                judge_1 = True
                judge_2 = True
                for point in double_dalian_1:
                    if state[point[0]][point[1]] != turn:
                        judge_1 = False
                for point in double_dalian_2:
                    if state[point[0]][point[1]] != turn:
                        judge_2 = False
                if not ((state[x+1][y+1] == turn and state[x+1][y+2] == 0) or (state[x+1][y+1] == 0 and state[x+1][y+2] == turn)):
                    judge_1 = False
                    judge_2 = False
                if judge_1 and judge_2:
                    for point in double_dalian_1:
                        processed_me.add(point)
                    for point in double_dalian_2:
                        processed_me.add(point)
                    len_double_dalian_me+=1
                elif judge_1:
                    for point in double_dalian_1:
                        processed_me.add(point)
                    len_double_dalian_me+=1
                elif judge_2:
                    for point in double_dalian_2:
                        processed_me.add(point)
                    len_double_dalian_me+=1
        for x in range(13):
            for y in range(11):
                double_dalian_1 = ((x,y),(x,y+3),
                                (x+1,y),(x+1,y+1),(x+1,y+2),(x+1,y+3))
                double_dalian_2 = ((x,y),(x,y+1),(x,y+2),(x,y+3),
                                (x+1,y),(x+1,y+3))
                judge_1 = True
                judge_2 = True
                for point in double_dalian_1:
                    if state[point[0]][point[1]] != turn or (point in processed_me):
                        judge_1 = False
                for point in double_dalian_2:
                    if state[point[0]][point[1]] != turn or (point in processed_me):
                        judge_2 = False
                if not ((state[x+1][y+1] == turn and state[x+1][y+2] == 0 and (not ((x+1,y+1) in processed_me))) or (state[x+1][y+1] == 0 and state[x+1][y+2] == turn and (not ((x+1,y+2) in processed_me)))):
                    judge_1 = False
                    judge_2 = False
                if judge_1:
                    for point in double_dalian_1:
                        processed_me.add(point)
                    len_double_dalian_me+=1
                elif judge_2:
                    for point in double_dalian_2:
                        processed_me.add(point)
                    len_double_dalian_me+=1
        #下面又复制了一遍上面的代码，把turn都改成了-turn，计算敌方双褡裢个数
        for x in range(12):
            for y in range(11):
                double_dalian_1 = ((x,y),(x,y+1),
                                    (x+1,y),(x+1,y+3),
                                    (x+2,y+2),(x+2,y+3))
                double_dalian_2 = ((x,y+2),(x,y+3),
                                    (x+1,y),(x+1,y+3),
                                    (x+2,y),(x+2,y+1))
                judge_1 = True
                judge_2 = True
                for point in double_dalian_1:
                    if state[point[0]][point[1]] != -turn:
                        judge_1 = False
                for point in double_dalian_2:
                    if state[point[0]][point[1]] != -turn:
                        judge_2 = False
                if not ((state[x+1][y+1] == -turn and state[x+1][y+2] == 0) or (state[x+1][y+1] == 0 and state[x+1][y+2] == -turn)):
                    judge_1 = False
                    judge_2 = False
                if judge_1 and judge_2:
                    for point in double_dalian_1:
                        processed_enemy.add(point)
                    for point in double_dalian_2:
                        processed_enemy.add(point)
                    len_double_dalian_enemy += 1
                elif judge_1:
                    for point in double_dalian_1:
                        processed_enemy.add(point)
                    len_double_dalian_enemy += 1
                elif judge_2:
                    for point in double_dalian_2:
                        processed_enemy.add(point)
                    len_double_dalian_enemy += 1
        for x in range(13):
            for y in range(11):
                double_dalian_1 = ((x,y),(x,y+3),
                                (x+1,y),(x+1,y+1),(x+1,y+2),(x+1,y+3))
                double_dalian_2 = ((x,y),(x,y+1),(x,y+2),(x,y+3),
                                (x+1,y),(x+1,y+3))
                judge_1 = True
                judge_2 = True
                for point in double_dalian_1:
                    if state[point[0]][point[1]] != -turn or (point in processed_enemy):
                        judge_1 = False
                for point in double_dalian_2:
                    if state[point[0]][point[1]] != -turn or (point in processed_enemy):
                        judge_2 = False
                if not ((state[x+1][y+1] == -turn and state[x+1][y+2] == 0 and (not ((x+1,y+1) in processed_enemy))) or (state[x+1][y+1] == 0 and state[x+1][y+2] == -turn and (not ((x+1,y+2) in processed_enemy)))):
                    judge_1 = False
                    judge_2 = False
                if judge_1:
                    for point in double_dalian_1:
                        processed_enemy.add(point)
                    len_double_dalian_enemy += 1
                elif judge_2:
                    for point in double_dalian_2:
                        processed_enemy.add(point)
                    len_double_dalian_enemy += 1
        for x in range(13):
            for y in range(13):
                block=((x,y),(x,y+1),(x+1,y),(x+1,y+1))
                blank = 0
                me = []
                enemy = []
                for point in block:
                    if state[point[0]][point[1]] == turn:
                        me.append(point)
                    elif state[point[0]][point[1]] == -turn:
                        enemy.append(point)
                    else:
                        blank += 1
                if len(me) == 3 and blank == 1:
                    len_triangle_me += 1
                    for p in me:
                        processed_me.add(p)
                elif len(enemy) == 3 and blank == 1:
                    len_triangle_enemy += 1
                    for p in enemy:
                        processed_enemy.add(p)
        if len_me > 14 and len_enemy <= 14:
            ret = (len_double_dalian_me*4 + len_me - len(processed_me)) / (len_double_dalian_me*4 + len_triangle_enemy*4 + len_me + len_enemy - len(processed_me) - len(processed_enemy))
        elif len_me <= 14 and len_enemy > 14:
            ret = (len_triangle_me*4 + len_me - len(processed_me)) / (len_double_dalian_enemy*4 + len_enemy + len_triangle_me*4 + len_me - len(processed_me) - len(processed_enemy))
        return ret


if __name__ == '__main__':
    g = Game()
    state=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-1, -1, -1, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0]]
    print('以下为测试数据:')
    cProfile.run("g.available_actions(state,1,'play')")
    text=str(g.available_actions(state, -1, 'play'))
    a=open('m.txt','w')
    a.write(text)
    a.close()
    print('作为棋子1，返回此时（对方进入飞子阶段）的胜率：',g.evaluate_in_ending_part(state, 1))
    print('作为棋子1，返回所有可行步骤：', g.available_actions(state, 1, 'play'))
    """
    print('作为棋子-1，返回所有可行步骤：', g.available_actions(state, -1, 'play'))
    action = (((0, 0), (0, 2)), ((0, 1),))
    state1 = g.next_state(state, action, 1, 'play')
    print('根据输入的action,返回棋盘下一状态:', state1)
    print('轮到棋子1下棋，判断棋局胜负是否已分，谁胜谁负：', g.end_game(state, 1, 'play'))
    print('轮到棋子-1下棋，判断棋局胜负是否已分，谁胜谁负：', g.end_game(state, -1, 'play'))
    print('作为棋子1，判断胜率：', g.evaluate(state, 1))
    print('作为棋子-1，判断胜率：', g.evaluate(state, -1))"""

"""
state
type:list list[list[number]]] 14*14
example:
[[1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
"""
