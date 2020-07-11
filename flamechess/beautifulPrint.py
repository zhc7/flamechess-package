import sys
sysprint = print


def beautifulPrint(state, action):
    printC = sys.stdout.shell.write
    route = action[0]
    eat = action[1]
    for x in range(len(state)):
        row = state[x]
        for y in range(len(row)):
            col = row[y]
            if (x, y) in route:
                print = lambda x: printC((x or '#') + ' ', "STRING")
            elif (x, y) in eat:
                print = lambda x: printC((x or '#') + ' ', "KEYWORD")
            else:
                print = lambda x: sysprint((x or ' '), end=' ')
            if col == -1:
                print('X')
            elif col == 1:
                print('O')
            else:
                print('')
            print = sysprint
        print()
