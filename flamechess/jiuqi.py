import itertools
class Game(object):
    def __init__(self):
        pass

    def available_actions(self, state, flag, me):
        """根据当前棋盘，对弈阶段和所执棋子返回可以下的坐标 
        return type:list example:[[步骤列表，提子列表]*n](play)  [[落子坐标/None,提子坐标/None]*n](layout)
        state:棋盘状态 
        flag:对弈阶段('layout':布局,'play':行棋)
        me:所执棋子 -1 or 1
        """
        def jump_action(start,state,me):
            '''使用递归，dfs搜索，输入起始点坐标，就地修改函数外的actions变量'''
            jump_points=self.points_can_jump(state,start,me)
            if jump_points:
                for point in jump_points:
                    if actions:
                        for action in actions:
                            if action[-1]==start:
                                actions.append(action[0:-1]+[start,point]) #将单一行棋合并到以初始起点为起点的行棋中
                    else: #start为初始起点时
                        actions.append([start,point])
                    state1=state
                    copystate=self.adjust_chessboard((start,point),state1,me) #编辑棋盘时复制一个新棋盘，不会瞎改原棋盘
                    jump_action(point,copystate,me)
        if flag == 'layout':  # 布棋阶段
            ret=[]
            blank_indexes = []  # 空白点坐标
            for index, status in enumerate(sum(state,[])):
                if status == 0:
                    row = index // 14
                    col = index - row * 14
                    blank_indexes.append((row, col))
            if len(blank_indexes) == 196:  # 如果所有都是空白，那么第一步必须下棋盘中央方格的对角线两端
                blank_indexes=[(6, 6), (6, 7), (7, 6), (7, 7)]
                for b in blank_indexes:
                    ret.append([b,None])
            elif len(blank_indexes) == 0: #如果所有格子都已经满了，那么说明该进入提子阶段了
                remove_indexes = []  # 可以移除的点的坐标
                for row, col in ((6, 6), (6, 7), (7, 6), (7, 7)):
                    if state[row][col] == me:
                        remove_indexes.append((row, col))
                for r in remove_indexes:
                    ret.append([None,r])
            else:
                for b in blank_indexes:
                    ret.append([b,None])
            return ret
            #flag为layout时
        elif flag == 'play':
            mine=[]
            blanks=[]
            for index, status in enumerate(sum(state,[])):
                if status == me:
                    row = index // 14
                    col = index - row * 14
                    mine.append((row,col))
                elif status==0:
                    row=index//14
                    col=index-row*14
                    blanks.append((row,col))
            all_actions=[]
            for one in mine:
                actions=[]
                actions_first_processed=[] #第一次处理（不包括褡裢）
                actions_last=[] #最后版本（考虑褡裢）
                state1=[]
                for l in state:
                    state1.append(l)
                jump_action(one,state1,me) #就地修改actions,加入所有跳棋步骤（不包括所有提子）
                for a in actions:
                    actions_first_processed.append(self.action_process(a)) #将跳棋步骤加入跳提子
                walks=self.go_around(one,state) #四周走棋
                for walk in walks:
                    actions_first_processed.append(walk) #四周走棋无需进行跳棋步骤的第一遍处理
                for a in actions_first_processed:
                    actions=self.find_dalian(state,a,me) #寻褡裢，返回包含了所有可能褡裢提子的步骤列表
                    for action in actions:
                        actions_last.append(action)
                for action in actions_last:
                    all_actions.append(action)
            if len(mine)<=14:
                went=[]
                for a in all_actions:
                    for w in a[0][1:]:
                        went.append(w)
                went=set(went)
                blanks=set(blanks)
                available=list(blanks-went) #求差集
                products=list(itertools.product(mine,available)) #组合
                for product in products:
                    product=[product,[]] #补提子的位
                    actions=self.find_dalian(state,product,me) #找褡裢
                    for action in actions:
                        all_actions.append(action)
            return all_actions

    def go_around(self,start,state):
        '''往四周行棋，接收初始坐标，返回所有行棋步骤，包括提子补位'''
        actions=[]
        row=start[0]
        col=start[1]
        possibilities=((row,col+1),(row,col-1),(row+1,col),(row-1,col))
        for possibility in possibilities:
            if 0 <= possibility[0] <=13 and 0 <= possibility[1] <= 13\
            and state[possibility[0]][possibility[1]]==0:
                actions.append([[start,possibility],[]]) #包含补位
        return actions

    def adjust_chessboard(self,action,state,me):
        '''根据单步跳棋调整棋盘，返回新棋盘'''
        state1=state #复制新棋盘
        start=action[0]
        end=action[1]
        remove=(int((start[0]+end[0])/2),int((start[1]+end[1])/2))
        state1[start[0]][start[1]]=0
        state1[end[0]][end[1]]=me
        state1[remove[0]][remove[1]]=0
        return state1

    def action_process(self,action):
        '''将只包含跳棋路线的步骤变为包含必提子的步骤'''
        removed=[]
        for i in range(len(action)-1):
            start=action[i]
            end=action[i+1]
            remove=((start[0]+end[0])/2,(start[1]+end[1])/2)
            removed.append(remove)
        return [action,removed]

    def find_dalian(self,state,action,me):
        '''找寻褡裢，接收行棋步骤（包括行棋中提子），返回新的行棋步骤列表（包括可以提的子）'''
        new_actions=[] #返回的行棋步骤列表
        n=0 #形成褡裢数
        remove=action[1] #这里即便不是跳棋，没有提子也必须补位
        start=action[0][0]
        end=action[0][-1]
        row,col=end[0],end[1] #获取终止点的行列
        state1=state
        state1[start[0]][start[1]]=0
        state1[row][col]=me
        for r in remove:
            state1[r[0]][r[1]]=0
        blocks=(((row,col),(row+1,col),(row+1,col+1),(row,col+1)),
        ((row,col),(row+1,col),(row+1,col-1),(row,col-1)),
        ((row,col),(row-1,col),(row-1,col-1),(row,col-1)),
        ((row,col),(row-1,col),(row-1,col+1),(row,col+1)))
        for block in blocks:
            try:
                judge=True
                for index in block:
                    row,col=index[0],index[1]
                    if state1[row][col]==0 or state1[row][col]!=me:
                        judge=False
                if judge:
                    n+=1
            except: #解决四个块中可能有坐标越界问题
                pass
        enemies=[] #敌方棋子坐标（可提）
        for index, status in enumerate(sum(state1,[])):
            if status!=me and status!=0:
                row = index // 14
                col = index - row * 14
                enemies.append((row,col))
        combinations=list(itertools.combinations(enemies,n)) #排列组合
        if combinations[0]: #如果没有褡裢，值将为 [()] ,需排除这种情况
            for removes in combinations:
                new_action=action
                for r in removes:
                    new_action[1].append(r)
                new_actions.append(new_action)
            return new_actions
        return [action] #若无褡裢，为了返回值的统一性，再外包一层列表
    
    def points_can_jump(self,state, index, me):
        '''输入棋子的坐标，返回元组形式的可跳的点的坐标'''
        row, col = index[0], index[1]
        judge=((row-1, col), (row+1, col), (row, col-1), (row, col+1))
        possible=((row-2, col), (row+2, col), (row, col-2), (row, col+2))
        can_jump=[]
        for judge,possible in zip(judge, possible):
            if 0 <= possible[0] <=13 and 0 <= possible[1] <= 13:
                row_j, col_j = judge[0], judge[1]
                row_p, col_p = possible[0],possible[1]
                if state[row_j][col_j] != 0 and state[row_j][col_j] != me and state[row_p][col_p] == 0:
                    can_jump.append((row_p, col_p))
        return can_jump

state=[[1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
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

g=Game()
print(g.available_actions(state,'play',1))



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
