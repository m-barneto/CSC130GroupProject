import time
import turtle


def draw_rect(x, y, size, col):
    t.goto(x, y)
    # set the fillcolor
    t.fillcolor(col)

    # start the filling color
    t.begin_fill()

    # drawing the square of side s
    for _ in range(4):
        t.forward(size)
        t.right(90)

    # ending the filling of the color
    t.end_fill()


def click(x, y):
    # Make sure valXX is referencing the global version
    global value_top_left
    global value_top_right
    global value_bottom_left
    global value_bottom_right

    # Animating check for future use, not sure if needed yet
    if not animating:
        # Check which corner the click was on, and set the value to .5, this will darken the color
        if x <= 0 and y <= 0:
            value_bottom_left = 0.5
            print("Bottom left")
        if x > 0 and y > 0:
            value_top_right = 0.5
            print("Top right")
        if x > 0 and y < 0:
            value_bottom_right = 0.5
            print("Bottom right")
        if x < 0 and y > 0:
            value_top_left = 0.5
            print("Top left")


def draw_tiles():
    # Draw all the squares with their respective colors
    draw_rect(0, 0, SQUARE_SIZE, (value_bottom_right, 0, 0))
    draw_rect(-SQUARE_SIZE, 0, SQUARE_SIZE, (0, value_bottom_left, 0))
    draw_rect(-SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, (0, 0, value_top_left))
    draw_rect(0, SQUARE_SIZE, SQUARE_SIZE, (value_top_right, value_top_right, 0))


WIDTH = 500
HEIGHT = 500
SQUARE_SIZE = WIDTH / 2

# Window setup
window = turtle.Screen()
window.title("Simon Says")
window.setup(width=WIDTH, height=HEIGHT)
# tracer(0) disables automatic screen updates (we'll be updating the screen ourselves)
window.tracer(0)
# Bind the onclick event to our click method
window.onclick(click)

# setup the turtle
t = turtle.Turtle()
t.speed(0)
t.penup()
t.hideturtle()

# Color animation variables
animating = False

value_top_left = 1
value_top_right = 1
value_bottom_left = 1
value_bottom_right = 1

while True:
    # Go through each color and add opacity back to it (TODO, move to own method)
    if value_top_left < 1:
        value_top_left = min(value_top_left + .099, 1.0)
    if value_top_right < 1:
        value_top_right = min(value_top_right + .099, 1.0)
    if value_bottom_left < 1:
        value_bottom_left = min(value_bottom_left + .099, 1.0)
    if value_bottom_right < 1:
        value_bottom_right = min(value_bottom_right + .099, 1.0)
    # Draw the tiles
    draw_tiles()
    # Update the window (may be possible to uncouple this from our sleep down below)
    window.update()
    # sleep for 1/15th of a second
    time.sleep(1 / 15)
