# our project code
import random
import time
import turtle
from turtle import Screen
import winsound
from tile import Tile
from listqueue import ListQueue
import sys



def set_intro_turtles(turtle_name: str, message: str):
    """Function to set up multiple turtles as individual cards for game and team intro
    @params: name of the turtle to be created and the message it puts on the card
    @returns: None"""
    # intro turtle:
    turtle_name = turtle.Turtle()
    turtle_name.color('red')
    style = ('Courier', 12, 'italic')
    turtle_name.write(message,
                font=style, align='center')
    turtle_name.speed(5) 
    turtle_name.penup()
    turtle_name.hideturtle()
    time.sleep(2)
    turtle_name.clear()

def call_intro():
    """
    This function sets up the intro turtles and their messages.
    """
    
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
    
    try:
        # loop through list and dict to generate series of intro cards
        for tur in turtle_msgs.keys():
            set_intro_turtles(tur, turtle_msgs[tur])
    except:
        print("Player ended the game.")
        sys.exit(1)
        
        
def set_tiles():
    """
    It creates four tiles, each with a different name, and returns them in a list
    :return: A list of tiles.
    """
    SQUARE_SIZE = 500 / 2
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
    return tiles

# global variables -> needed for the click method that doesn't take params other than the x,y coordinates from the click
state = {'state': "Playing Sequence"}
# States:
# Playing Sequence
# Player Turn
# Animating
clicked_tile = None

# set the tiles for both the click method and the play game method
tiles = set_tiles()


def create_sequence():
    """
    The function create_sequence() creates a random sequence of 4 numbers between 0 and 3
    :return: A list of 4 random numbers between 0 and 3.
    """
    
    # create a random sequence for the computer to play 
    seq = []
    for i in range(4):
        num = random.randrange(0,4)
        seq.append(num)
    return seq



def set_window():
    """
    It creates a turtle screen, sets the title to "Simon Says", sets the width and height to 500, and
    disables automatic screen updates.
    :return: The window is being returned.
    """
    
    # Window setup
    WIDTH = 500
    HEIGHT = 500
    window = Screen()
    window.title("Simon Says")
    window.setup(width=WIDTH, height=HEIGHT)
    # tracer(0) disables automatic screen updates (we'll be updating the screen ourselves)
    window.tracer(0)
    return window




def set_score_turtle():
    """
    It creates a score turtle, sets its position, hides it, sets its color, and sets its width
    :return: The score_t turtle is being returned.
    """
    
    # set up score turtle
    score_t = turtle.Turtle()
    score_t.penup()
    score_t.setposition(0,0)
    score_t.hideturtle()
    score_t.color("red")
    score_t.width(10)
    return score_t

def set_main_turtle():
    """
    It returns the main turtle object that is set up to draw instantly and is hidden.
    :return: The turtle object.
    """
    
    # Setup the tiles turtle
    t = turtle.Turtle()
    # Make it draw instantly
    t.speed(0)
    # Hide the turtle
    t.penup()
    t.hideturtle()
    return t

def click(x, y):
    """
    If the player clicks on a tile, play a sound and set the clicked_tile variable to the index of the
    tile
    
    :param x: The x coordinate of the click
    :param y: The y coordinate of the click
    :return: The index of the tile that was clicked
    """
    # Only register clicks during the player's turn
    if state['state'] != "Player Turn":
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


def play_sequence(t,window,sequence):
    """
    It loops through the items in the sequence, plays a sound, and animates the tile
    
    :param t: The time in seconds since the program started
    """
    
    # Loop through the tiles in the sequence
    for item in sequence.items:
        # Make a sound
        winsound.Beep((item * 100) + 1000, 250)
        # Animate the tile
        tiles[item].animate_fade(t, window)


def play_game():
    """
    The function runs the game: it sets up the main turtle and the score turtle, then it enters a while loop that draws the tiles, plays the sequence, copies the sequence to a player_seq listqueue, adds a new number to the sequence, changes the state to player's turn, waits for input, checks if the player clicked on the a tile that isnt the next in the player_seq queue, changes state to animating, animates the tile
    at the top of the queue, switches state back to player's turn, resets clicked_tile variable, checks if the player has input all the tiles correctly, sets state to playing sequence, adds 1 to score,
    shows the score constantly on the top of the screen, shows the score in the middle of the screen for each round, and then sleeps for a second
    """
    window = set_window()
    t = set_main_turtle()
    score_t = set_score_turtle()   
    score = 0
    # create the computer sequence and the player sequence
    sequence = ListQueue(create_sequence())
    player_seq = ListQueue(sequence.items)
    # reset the global variable values
    global clicked_tile
    # Try block to catch closing the window unexpectedly
    try:
        while True:
            # Draw each tile
            for j in tiles:
                j.draw(t)
            # Render the draw calls to the window
            window.update()

            if state['state'] == "Playing Sequence":
                # Sleep for a second before playing sequence
                time.sleep(1)
                # Play the sequence
                play_sequence(t, window, sequence)
                # Copy the sequence to a player_seq listqueue
                player_seq = ListQueue(sequence.items)
                # Add a new number to the sequence
                sequence.add(random.randrange(0, 4))
                # Change the state to player's turn
                state.update({'state' : "Player Turn"})
            elif state['state'] == "Player Turn":
                # Bind the onclick event to our click method
                window.onclick(click)
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
                
                state.update({"state": "Animating"})
                # Animate the tile at the top of the queue
                tiles[player_seq.pop()].animate_fade(t, window)
                # Switch state back to player's turn
                state.update({'state': "Player Turn"})
                # Reset clicked_tile variable
                clicked_tile = None
                
                # If the player has input all the tiles correctly
                if player_seq.isEmpty():
                    # Set state to playing sequence
                    state.update({'state' : "Playing Sequence"})
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


def main():
    call_intro()
    play_game()


if __name__ == "__main__":
    main()