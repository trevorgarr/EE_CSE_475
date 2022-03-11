import asyncio
import chess

piece_colors = {
    'r': (255, 50, 0),
    'n': (255, 150, 0),
    'b': (255, 255, 0),
    'q': (125, 50, 0),
    'k': (125, 150, 0),
    'p': (175, 255, 0),

    'R': (0, 50, 255),
    'N': (0, 150, 255),
    'B': (0, 255, 255),
    'Q': (0, 50, 125),
    'K': (0, 150, 125),
    'P': (0, 255, 125),
    '.': (0, 0, 0)
}

def color(red, green, blue):
    return (red << 16) | (green << 8) | blue


class ChessApp:
    def __init__(self):
        self.Board = chess.Board()
        self.touch_grid = [(0, 0, 0)] * 192
        self.move_state = 0  # 0 - selecting piece, 1 - selecting move
        self.move_options = []
        self.selected_piece = 0
        self.check_mate = 0
        self.board_state = []
        self.IS_TIMER_BASED = False
        self.SPEED = 1
        self.setup_chess()

    def convert(self, x, y):
        # if in an odd column, reverse the order
        if (x % 2 != 0):
            y = 15 - y
        return (x * 16) + y

    def chess_convert(self, x, y):
        n = x * 8 + y
        location_code = chr(y + 97) + str(x + 1)
        return n, location_code

    def chess_convert_to_index(self, string_val):
        x = int(string_val[1]) - 1
        y = ord(string_val[0]) - 97
        return x, y
    # https://stackoverflow.com/questions/5661725/format-ints-into-string-of-hex

    def rgb_to_hex(self, r, g, b):
        numbers = [r, g, b]
        return '#' + ''.join('{:02X}'.format(a) for a in numbers)

    def setup_chess(self):
        print("chess start")
        self.board_state = str(self.Board).replace('\n', ' ').split(' ')
        for x in range(1, 9):
            for y in range(8):
                self.touch_grid[self.convert(
                    x - 1, y)] = piece_colors[self.board_state[(8 - x) * 8 + y]]
        # print(self.board_state)

    async def get_grid(self):
        return self.touch_grid

    def web_paint(self, n, web_color):
        x = int(n / 16)
        y = int(n - x * 16)
        self.paint(x, y)

    def update_board(self):
        self.board_state = str(self.Board).replace('\n', ' ').split(' ')
        for x in range(1, 9):
            for y in range(8):
                self.touch_grid[self.convert(
                    x - 1, y)] = piece_colors[self.board_state[(8 - x) * 8 + y]]

    def paint(self, x, y):
        n, location_code = self.chess_convert(x, y)

        if (location_code not in self.move_options):
            self.move_state = 0
            self.selected_piece = location_code
        else:
            self.move_state = 1
        if (self.move_state == 0):
            for i, x in enumerate(list(self.Board.legal_moves)):
                # print(x)
                if (str(x)[0:2] == location_code):
                    newX, newY = self.chess_convert_to_index(str(x)[2:4])
                    self.touch_grid[self.convert(newX, newY)] = (0, 255, 255)
                    self.move_options.append(str(x)[2:4])
        if (self.move_state == 1):
            move = chess.Move.from_uci(
                str(self.selected_piece) + str(location_code))
            # print(move)
            self.Board.push(move)
            self.update_board()
            self.selected_piece = 0
            self.move_options = []
            self.move_state = 0
        # print(self.move_options)
