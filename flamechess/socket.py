import socketio


class Client(socketio.Client):
    def __init__(self, gameId, userId, url="https://chessterm.tech:8512"):
        super(Client, self).__init__()
        self.gameId = gameId
        self.userId = userId
        self.data = None
        self.chesspos = None
        self.on("connect", self.on_connect)
        self.on("login_result", self.on_login)
        self.on("update_chesspos", self.on_update)
        self.connect(url)

    def on_connect(self):
        self.emit("login", (self.sid, {
            "backend": "https://chessterm.tech",
            "userId": self.userId,
            "gameId": self.gameId
        }))

    def on_login(self, data):
        self.data = data

    def on_update(self, chesspos):
        self.chesspos = chesspos

    def set_data(self, chesspos):
        self.emit("update_board", (self.sid, {
            "chesspos": chesspos
        }))

    def get_data(self):
        return self.chesspos


if __name__ == '__main__':
    client = Client(1002, 10170101)
    last_board = client.get_data()
    while True:
        board = client.get_data()
        if board != last_board:
            print(board)
            client.set_data('000000ZZZ0000000zzz000000')
        last_board = board
