class Game(object):
    def __init__(self):
        pass

    def available_actions(self, state, flag, me):
        """根据当前棋盘，对弈阶段和所执棋子返回可以下的坐标 
        return type:tuple example:(((起始坐标,终止坐标)*m),(移除棋子坐标*n))
        state:棋盘状态 
        flag:对弈阶段('layout':布局,'remove':移去棋盘中央方格的对角线两端的棋子,'play':行棋)
        me:所执棋子 'Z' or 'z'
        """
        if flag == 'layout':  # 布棋阶段
            blank_indexes = []  # 空白点坐标
            for index, status in enumerate(''.join(state)):
                if status == '0':
                    row = index // 14
                    col = index - row * 14
                    blank_indexes.append((row, col))
            if len(blank_indexes) == 196:  # 如果所有都是空白，那么第一步必须下棋盘中央方格的对角线两端
                blank_indexes = [(6, 6), (6, 7), (7, 6), (7, 7)]
            ret = (tuple((None, i) for i in blank_indexes), None)
        elif flag == 'remove':
            remove_indexes = []  # 可以移除的点的坐标
            for row, col in ((6, 6), (6, 7), (7, 6), (7, 7)):
                if state[row][col] == me:
                    remove_indexes.append((row, col))
            ret = (None, tuple(remove_indexes))
        elif flag == 'play':
            pass


"""
state
type:list list[str]
example:['Zz000000000000', '00000000000000', 
'00000000000000', '00000000000000', 
'00000000000000', '00000000000000', 
'00000000000000', '00000000000000', 
'00000000000000', '00000000000000', 
'00000000000000', '00000000000000', 
'00000000000000', '00000000000000']
"""
