# import RPi.GPIO as GPIO
# import time
import numpy as np
import curses

# PWM OUTPUT
# ledN = 1
# ledW = 2
# ledS = 3
# ledE = 4

# Initialization
def setup():
    window = curses.initscr()
    curses.noecho()
    window.keypad(True)
    return window

def printToScreen(window, text, y=1):
    window.addstr(y, 0, text, curses.A_REVERSE)
    window.refresh()

# Loop
def loop(window):
    while True:
        sequence = getRandomSequence(5)
        song = 1;
        printToScreen(window, str(sequence), 0)
        startAttempt(sequence, window)
        printToScreen(window, "new sequence is generated")


def getDirection(k):
    if k == 259:
        return 'N'
    if k == 258:
        return 'S'
    if k == 260:
        return 'W'
    if k == 261:
        return 'E'

def startAttempt(sequence, window):
    for current_direction in sequence:
        k = window.get_wch()
        current_input = getDirection(k)

        if current_input != current_direction:
            # reset attempt if direction is wrong
            printToScreen(window, 'wrong')
            startAttempt(sequence, window)
            return
        else:
            printToScreen(window, 'right')

        curses.flushinp()
    printToScreen(window, 'sequence complete')

def playSong():
    return 0

# Return a list of a certain length filled with directions
def getRandomSequence(length):

    directions = ['N', 'W', 'S', 'E']
    seq = np.random.choice(directions, length).tolist()

    return seq

# Execution
window = setup()
loop(window)
