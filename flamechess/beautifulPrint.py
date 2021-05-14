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


def log_parser(logFile):
    try:
        with open(logFile, encoding="utf-8") as f:
            log = f.readlines()
    except (FileNotFoundError, OSError):
        log = logFile.split('\n')
    states = []
    actions = []
    state = []
    for line in log:
        if not line or line[2:4] not in ["O ", "X ", "- "]:
            if line and line[:9] == 'Actions: ':
                actions.append(line[9:])
            if state:
                states.append(state)
            state = []
            continue
        row = []
        line = line[2:]
        for item in line.split(' '):
            item = item.strip()
            if not item:
                continue
            row.append({"O":1, "X":-1, "-":0}[item])
        state.append(row)
    return states, actions


def differencePrinter(states, actions=None):
    last_state = states[0]
    printC = sys.stdout.shell.write
    for i in range(len(states)):
        state = states[i]
        if not state:
            continue
        for x in range(len(state)):
            row = state[x]
            last_row = last_state[x]
            for y in range(len(row)):
                col = row[y]
                last_col = last_row[y]
                if col != last_col:
                    printC({1:'O', -1:'X', 0:'#'}[col] + " ", "KEYWORD")
                else:
                    printC({1: 'O', -1: 'X', 0: '-'}[col] + " ")
            print()
        if actions:
            print(actions[i])
        last_state = state
        input()


if __name__ == '__main__':
    differencePrinter(*log_parser("../alphaZero/log.txt"))

