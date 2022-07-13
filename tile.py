import time
import turtle
import sys


class Tile:

    def __init__(self, x: float, y: float, size: float, tile_pos_name: str):
        self.x = x
        self.y = y
        self.size = size
        self.tile_pos_name = tile_pos_name

        self.fade_value = 1.0

    def update_fade(self) -> None:
        #                                 (1.0 - 0.2) / steps
        self.fade_value = min(self.fade_value + (.8 / 2), 1.0)

    def get_color(self) -> tuple:
        if self.tile_pos_name == "Top Left":
            return (0, 0, self.fade_value)
        elif self.tile_pos_name == "Top Right":
            return (self.fade_value, self.fade_value, 0)
        elif self.tile_pos_name == "Bottom Left":
            return (0, self.fade_value, 0)
        elif self.tile_pos_name == "Bottom Right":
            return (self.fade_value, 0, 0)

    def draw(self, t: turtle.Turtle) -> None:
        t.goto(self.x, self.y)
        # set the fillcolor
        color = self.get_color()
        t.fillcolor(color)

        # start the filling color
        t.begin_fill()

        # drawing the square of side s
        for _ in range(4):
            t.forward(self.size)
            t.right(90)

        # ending the filling of the color
        t.end_fill()

    def handle_click(self, mouse_x: float, mouse_y: float) -> bool:
        """
        if (    mouse_x > self.x and
                mouse_y < self.y and
                mouse_x <= self.x + self.size and
                mouse_y >= self.y - self.size):
        """
        if (self.x < mouse_x <= self.x + self.size and
                self.y > mouse_y >= self.y - self.size):
            return True
        else:
            return False

    def animate_fade(self, t: turtle.Turtle, window: turtle.TurtleScreen, anim_duration: float) -> None:
        self.fade_value = 0.2
        try:
            if self.fade_value < 1.0:
                for _ in range(2):
                    self.update_fade()
                    self.draw(t)
                    window.update()
                    time.sleep(anim_duration / 2)
                self.fade_value = 1.0
        except Exception as e:
            print("Player ended the game.")
            sys.exit(1)
