import asyncio
#from rpi_ws281x import Color

class MenuApp:
    def __init__(self, device_id):
        self.device_id = device_id
        self.next_app = ''
        self.app_array = ['Painting', 'tictactoe', 'chess', 'animation',
                         'Brick Shooter', 'Tug of War', 'Simon Says', 'Pong', 'Image Show', 'Stacker']
        self.new_app_selected = 0
        self.touch_grid = [(0, 0, 0)] * 192
        self.IS_TIMER_BASED = False
        self.SPEED = 1

    def display_number(self, number, start_x, start_y):

        array = [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1]
        if number == 1:
            array = [0, 0, 1,
                     0, 0, 1,
                     0, 0, 1,
                     0, 0, 1,
                     0, 0, 1]

        if number == 2:
            array = [1, 1, 1,
                     0, 0, 1,
                     1, 1, 1,
                     1, 0, 0,
                     1, 1, 1]

        if number == 3:
            array = [1, 1, 1,
                     0, 0, 1,
                     1, 1, 1,
                     0, 0, 1,
                     1, 1, 1]

        if number == 4:
            array = [1, 0, 1,
                     1, 0, 1,
                     1, 1, 1,
                     0, 0, 1,
                     0, 0, 1]

        if number == 5:
            array = [1, 1, 1,
                     0, 0, 1,
                     1, 1, 1,
                     1, 0, 0,
                     1, 1, 1]

        if number == 6:
            array = [1, 1, 1,
                     1, 0, 0,
                     1, 1, 1,
                     1, 0, 1,
                     1, 1, 1]

        if number == 7:
            array = [1, 1, 1,
                     0, 0, 1,
                     0, 0, 1,
                     0, 0, 1,
                     0, 0, 1]

        if number == 8:
            array = [1, 1, 1,
                     1, 0, 1,
                     1, 1, 1,
                     1, 0, 1,
                     1, 1, 1]

        if number == 9:
            array = [1, 1, 1,
                     1, 0, 1,
                     1, 1, 1,
                     0, 0, 1,
                     0, 0, 1]

        for i in range(0, 5):
            for j in range(0, 3):

                if (array[i * 3 + j] == 1):
                    self.touch_grid[self.convert(
                        start_x + j, start_y + i)] = (255, 255, 255)
                else:
                    self.touch_grid[self.convert(
                        start_x + j, start_y + i)] = (0, 0, 0)

    def convert(self, x, y):
        # if in an odd column, reverse the order
        if (x % 2 != 0):
            y = 15 - y
        return (x * 16) + y

    # https://stackoverflow.com/questions/5661725/format-ints-into-string-of-hex
    def rgb_to_hex(self, r, g, b):
        numbers = [r, g, b]
        return '#' + ''.join('{:02X}'.format(a) for a in numbers)

    def setup_menu(self):
        self.new_app_selected = 0
        self.selectedApp = ''
        self.display_number(int(self.device_id % 10), 2, 2)
        self.display_number(int(self.device_id / 10), 6, 2)

        self.touch_grid[self.convert(2, 10)] = (255, 0, 255)
        self.touch_grid[self.convert(3, 10)] = (255, 255, 255)
        self.touch_grid[self.convert(4, 10)] = (255, 255, 0)
        self.touch_grid[self.convert(5, 10)] = (0, 0, 255)
        self.touch_grid[self.convert(6, 10)] = (0, 255, 0)
        self.touch_grid[self.convert(7, 10)] = (0, 255, 255)
        self.touch_grid[self.convert(8, 10)] = (0, 255, 170)
        self.touch_grid[self.convert(9, 10)] = (255, 120, 0)
        self.touch_grid[self.convert(2, 11)] = (255, 0, 120)
        self.touch_grid[self.convert(3, 11)] = (120, 120, 255)

    async def get_grid(self):
        return self.touch_grid

    def web_paint(self, n):
        x = int(n / 16)
        y = int(n - x * 16)
        print(x, y)
        print(self.convert(x, y))

    def paint(self, x, y):
        print(x, y)
        if y == 10:
            if (x >= 2 and x <= 9):
                self.next_app = self.app_array[x - 2]
                self.new_app_selected = 1
        if y == 11:
            if (x >= 2 and x <= 3):
                self.next_app = self.app_array[x + 6]
                self.new_app_selected = 1
        print(self.next_app)
