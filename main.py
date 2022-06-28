import random
import time
import turtle
import winsound

from tile import Tile
from listqueue import ListQueue


WIDTH = 500
HEIGHT = 500
SQUARE_SIZE = WIDTH / 2

# Window setup
window = turtle.Screen()
window.title("Simon Says")
window.setup(width=WIDTH, height=HEIGHT)
# tracer(0) disables automatic screen updates (we'll be updating the screen ourselves)
window.tracer(0)


def set_up_turtles(turtle_name: str, message: str):
    """Function to set up multiple turtle as individual cards for game and team intro
    @params: name of the turtle to be created and the message it puts on the card
    @returns: None"""
    # set up intro turtle:
    turtle_name = turtle.Turtle()
    turtle_name.color('red')
    style = ('Courier', 12, 'italic')
    turtle_name.write(message,
                font=style, align='center')
    turtle_name.speed(5) 
    # Let us see how many rounds you go!',
    turtle_name.penup()
    turtle_name.hideturtle()
    time.sleep(2)
    turtle_name.clear()

def call_intro():
    # set up and run the intro turtles dict:
    turtle_msgs = { "intro_t1": "Come play Simon Says with us!",
                "intro_t2": "Click on each tile in the same sequence",
                "intro_t3": "Lets see how many rounds you go!",
                "intro_t4": "Team:",
                "intro_t5": "Matthew Barneto",
                "intro_t6" : "Kristena Bridges",
                "intro_t7" : "Jonathan Alvarado",
                "intro_t8" : "Sowmya Aji",
                "intro_t9" : "Have fun!"
            }
    # loop through list and dict to generate series of intro cards
    for tur in turtle_msgs.keys():
        set_up_turtles(tur, turtle_msgs[tur])
        

call_intro()
# Setup the tiles turtle
t = turtle.Turtle()
# Make it draw instantly
t.speed(0)
# Hide the turtle
t.penup()
t.hideturtle()


# Setup tiles
tile_top_left = Tile(-SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, "Top Left")
tile_top_right = Tile(0, SQUARE_SIZE, SQUARE_SIZE, "Top Right")
tile_bottom_left = Tile(-SQUARE_SIZE, 0, SQUARE_SIZE, "Bottom Left")
tile_bottom_right = Tile(0, 0, SQUARE_SIZE, "Bottom Right")

tiles = [
    tile_top_left,  # 0
    tile_top_right,  # 1
    tile_bottom_left,  # 2
    tile_bottom_right  # 3
]

state = "Playing Sequence"
# States:
# Playing Sequence
# Player Turn
# Animating


sequence = ListQueue([0, 1, 3])
player_seq = ListQueue(sequence.items)
clicked_tile = None


# set up score turtle
score_t = turtle.Turtle()
score_t.penup()
score_t.setposition(0,0)
score_t.hideturtle()
score_t.color("red")
score_t.width(10)
score = 0


def click(x, y):
    # Only register clicks during the player's turn
    if state != "Player Turn":
        return

    global clicked_tile
    # Loop through the tiles
    for i in range(len(tiles)):
        # If the click lands on the tile
        if tiles[i].handle_click(x, y):
            # Play a sound
            winsound.Beep((i * 100) + 1000, 250)
            # Set clicked_tile to the index of the tile
            clicked_tile = i
            # Break out of the for loop as the clicked tile has already been found
            break


# Bind the onclick event to our click method
window.onclick(click)


def play_sequence():
    # Loop through the tiles in the sequence
    for item in sequence.items:
        # Make a sound
        winsound.Beep((item * 100) + 1000, 250)
        # Animate the tile
        tiles[item].animate_fade(t, window)


# Try block to catch closing the window unexpectedly
try:
    while True:
        
        # Draw each tile
        for j in tiles:
            j.draw(t)
        # Render the draw calls to the window
        window.update()

        if state == "Playing Sequence":
            # Sleep for a second before playing sequence
            time.sleep(1)
            # Play the sequence
            play_sequence()
            # Copy the sequence to a player_seq listqueue
            player_seq = ListQueue(sequence.items)
            
            # Add a new number to the sequence
            sequence.add(random.randrange(0, 4))
            # Change the state to player's turn
            state = "Player Turn"
        elif state == "Player Turn":
            # Wait for input
            while clicked_tile is None:
                # this should wait until our click method is called, which will set clicked_tile to an integer
                window.update()

            # If the player clicked on the a tile that isnt the next in the player_seq queue
            if player_seq.peek() != clicked_tile:
                # End the game
                print(f"Player ended game with {score} points!")
                break
            # Change state to animating that way clicks during this time will be ignored
            state = "Animating"
            # Animate the tile at the top of the queue
            tiles[player_seq.pop()].animate_fade(t, window)
            # Switch state back to player's turn
            state = "Player Turn"
            # Reset clicked_tile variable
            clicked_tile = None
            # If the player has input all the tiles correctly
            if player_seq.isEmpty():
                # Set state to playing sequence
                state = "Playing Sequence"
                # Add 1 to score
                score += 1
                # show the score constantly on the top of the screen
                window.title(f"Simon says: Player current score: { score }")
                t.hideturtle()
                # show the score in the middle of the screen for each round
                score_t.write(f"Score: { score }", font=('Arial', 15, 'bold'), align="center")
                time.sleep(1)
                score_t.clear()
                
except turtle.Terminator:
    print("Player ended the game.")
